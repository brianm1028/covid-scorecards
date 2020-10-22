from . import DistrictDataCache
import requests
from datetime import datetime, timedelta
import pprint
from sqlalchemy import and_
from ..models import TATMetrics
from ..models import CLIMetrics
from ..models import INCMetrics

pp = pprint.PrettyPrinter(indent=4)

def date_str(d=0):
    td = timedelta(days=d)
    d = datetime.today() - td
    s = '{mon}/{day}/{yr}'.format(day=d.day,mon=d.month,yr=d.year)
    return s


def date_in_window(dv, td):
    d = datetime.strptime(dv, '%m/%d/%Y')
    return (d <= datetime.today()) and (d >= (datetime.today() - td))


class GeoDataCache(DistrictDataCache):

    def __init__(self, district_id='3404906700000', dc=None):
        if dc is not None:
            super().__init__(dc=dc)
        else:
            super().__init__(district_id=district_id)

        self.county_list = self.load_county_list()
        self.covid_historical_test_results = self.load_covid_hist_test_data()
        for i in range(len(self.covid_historical_test_results['historical_county']['values'])):
            if 'testdate' in self.covid_historical_test_results['historical_county']['values'][i]:
                self.covid_historical_test_results['historical_county']['values'][i]['testDate']=self.covid_historical_test_results['historical_county']['values'][i]['testdate']
        self.covid_zip = self.load_covid_zip_data(days=self.configuration.config()["geo"]["zip_duration"])

        self.zip_positivity = self.calculate_zip_positivity(days=self.configuration.config()["geo"]["zip_duration"])
        self.county_positivity = self.calculate_county_positivity(days=self.configuration.config()["geo"]["county_duration"])
        self.region_positivity = self.calculate_region_positivity(days=self.configuration.config()["geo"]["region_duration"])

        self.county_incidence = self.calculate_county_incidence(
            dur_days=self.configuration.config()["geo"]["county_inc_duration"],
            avg_days=self.configuration.config()["geo"]["county_inc_average"])

        self.cli_metrics = self.calculate_health_system_capacity(
            dur_days=self.configuration.config()["geo"]["county_cli_duration"])
        self.tat_metrics = self.calculate_testing_turnaround_time(
            dur_days=self.configuration.config()["geo"]["county_tat_duration"])

        print(self.county_incidence)
        print(self.cli_metrics)
        print(self.tat_metrics)

    @staticmethod
    def load_county_list():
        r = requests.get('https://www.dph.illinois.gov/sitefiles/CountyList.json?nocache=1')
        return r.json()

    @staticmethod
    def load_covid_hist_test_data():
        r = requests.get('https://www.dph.illinois.gov/sitefiles/COVIDHistoricalTestResults.json?nocache=1')
        return r.json()

    @staticmethod
    def load_covid_zip_data(days=3):
        data = {
            'LastUpdateDate': {
                'year': datetime.today().year,
                'month': datetime.today().month,
                'day': datetime.today().day
            },
            'historical_zip': {
                'values': []
            }
        }
        for d in range(days+1):

            url = 'http://lfschools.bsmartin.info.s3-website-us-east-1.amazonaws.com/zip_data/{date}.json'.format(
                date=datetime.strftime(datetime.today() - timedelta(days=d), '%Y-%m-%d')
            )
            r = requests.get(url)
            resp_data = r.json()
            rec = {
                'testDate': date_str(d),
                'values': []
            }
            for zv in resp_data['zip_values']:
                zr = {
                    "zip": zv['zip'],
                    'confirmed_cases': zv['confirmed_cases'],
                    'total_tested': zv['total_tested']
                }
                rec['values'].append(zr)

            data['historical_zip']['values'].append(rec)

        return data

    def calculate_county_incidence(self, avg_days=7, dur_days=7):
        # number of new confirmed cases per 100k county population
        # 7 day rolling average, rounded whole for 7 consecutive days
        # remote is >14, hybrid is 7-14, in-person is <7


        data = {}
        for d in range(dur_days + avg_days + 1):
            data[d] = {}
            for dv in [r for r in self.covid_historical_test_results['historical_county']['values']
                if r['testDate'] == date_str(d + 3)]:
                    for cv in [c for c in dv['values'] if c['County'] in self.counties.keys()]:
                        data[d][cv['County']] = {
                            'confirmed_cases': cv['confirmed_cases'],
                            'total_tested': cv['total_tested'],
                            'testDate': dv['testDate']
                        }
        p = {}
        population = {}
        for d in range(dur_days + avg_days):
            p[d] = {}
            for c in self.counties.keys():
                p[d][c] = {
                    'confirmed_cases': (data[d][c]['confirmed_cases'] - data[d + 1][c]['confirmed_cases']),
                    'incidence': (data[d][c]['confirmed_cases'] - data[d + 1][c]['confirmed_cases'])/self.counties[c].population*100000,
                    'total_tested': (data[d][c]['total_tested'] - data[d + 1][c]['total_tested']),
                    'testDate': data[d][c]['testDate']
                }
                if p[d][c]['total_tested']>0:
                    p[d][c]['positivity_rate'] = p[d][c]['confirmed_cases'] / p[d][c]['total_tested']
                else:
                    p[d][c]['positivity_rate'] = 0
                p[d]['testDate'] = p[d][c]['testDate']
                population[c]=self.county_list['countyValues']
        for d in range(dur_days):
            for c in self.counties.keys():
                p[d][c]['dur_roll_avg_incidence']=sum([p[d+ad][c]['incidence'] for ad in range(avg_days)])/avg_days

        return p

    def calculate_health_system_capacity(self,dur_days=7):
        # number of covid like admissions across all ages from NSSP
        # number of days of non-increasing value out of the past 10 days
        # remote is <7, hybrid and in-person is 7 or more
        cli_data_lag = 5
        cli_data = CLIMetrics.query.filter(and_(
            CLIMetrics.update_date>=datetime.today()-timedelta(days=dur_days+1+cli_data_lag),
            CLIMetrics.update_date<datetime.today()-timedelta(days=cli_data_lag)
        )).all()

        p={}
        for cli_dp in cli_data:
            d=(datetime.today() - cli_dp.update_date).days-cli_data_lag
            p[d]={
                cli_dp.county_name:{
                    'cli_admissions':cli_dp.value
                },
                'testDate':cli_dp.update_date.strftime("%#m/%d/%Y")
            }
        return p

    def calculate_testing_turnaround_time(self,dur_days=7):
        # average number of days from sample collection to result entry in ELRS
        # 7 day rolling average, rounded whole, three day lag
        # remote is >10 days, hybrid is 3-10 days, in-person is <3 days
        tat_data_lag = 3
        tat_data = TATMetrics.query.filter(and_(
            TATMetrics.update_date>=datetime.today()-timedelta(days=dur_days+tat_data_lag),
            TATMetrics.update_date<datetime.today()-timedelta(days=tat_data_lag)
        )).all()

        p={}
        for tat_dp in tat_data:
            d=(datetime.today() - tat_dp.update_date).days-tat_data_lag
            p[d]={
                tat_dp.county_name:{
                    'tat_days':tat_dp.value
                },
                'testDate':tat_dp.update_date.strftime("%#m/%d/%Y")
            }
        return p

    def calculate_zip_positivity(self, days=3):
        data = {}
        for d in range(days+1):
            data[d] = {}
            for dv in [r for r in self.covid_zip['historical_zip']['values'] if r['testDate'] == date_str(d)]:
                for zv in [z for z in dv['values'] if int(z['zip']) in list(self.zip_codes.keys())]:
                    data[d][int(zv['zip'])] = {
                        'confirmed_cases': zv['confirmed_cases'],
                        'total_tested': zv['total_tested'],
                        'testDate': dv['testDate']
                    }
        p = {}
        for d in range(days):
            p[d] = {}
            for z in self.zip_codes.keys():
                p[d][z] = {
                    'confirmed_cases': (data[d][z]['confirmed_cases']-data[d+1][z]['confirmed_cases']),
                    'total_tested': (data[d][z]['total_tested']-data[d+1][z]['total_tested']),
                    'testDate': data[d][z]['testDate']
                }
                if p[d][z]['total_tested'] > 0:
                    p[d][z]['positivity_rate'] = p[d][z]['confirmed_cases'] * 10000 / self.zip_codes[z].population
                else:
                    p[d][z]['positivity_rate'] = 0
                p[d]['testDate'] = p[d][z]['testDate']
        return p

    def calculate_county_positivity(self, days=3):
        data = {}
        for d in range(days+1):
            data[d] = {}
            for dv in [r for r in self.covid_historical_test_results['historical_county']['values']
                       if r['testDate'] == date_str(d+3)]:
                for cv in [c for c in dv['values'] if c['County'] in self.counties.keys()]:
                    data[d][cv['County']] = {
                        'confirmed_cases': cv['confirmed_cases'],
                        'total_tested': cv['total_tested'],
                        'testDate': dv['testDate']
                    }

        p = {}
        for d in range(days):
            p[d] = {}
            for c in self.counties.keys():
                p[d][c] = {
                    'confirmed_cases': (data[d][c]['confirmed_cases']-data[d+1][c]['confirmed_cases']),
                    'total_tested': (data[d][c]['total_tested']-data[d+1][c]['total_tested']),
                    'testDate': data[d][c]['testDate']
                }
                if p[d][c]['total_tested']>0:
                    p[d][c]['positivity_rate'] = p[d][c]['confirmed_cases'] / p[d][c]['total_tested']
                else:
                    p[d][c]['positivity_rate'] = 0
                p[d]['testDate'] = p[d][c]['testDate']
        return p

    def calculate_region_positivity(self, days=3):
        p = {}
        for d in range(days):
            p[d] = {}
            p[d][self.COVIDRegion.id] = {
                'confirmed_cases': 0,
                'total_tested': 0,
                'testDate': ''
            }
            for c in self.counties:
                p[d][self.COVIDRegion.id]['confirmed_cases'] += self.county_positivity[d][c]['confirmed_cases']
                p[d][self.COVIDRegion.id]['total_tested'] += self.county_positivity[d][c]['total_tested']
                p[d][self.COVIDRegion.id]['testDate'] = self.county_positivity[d][c]['testDate']
            p[d][self.COVIDRegion.id]['positivity_rate'] = p[d][self.COVIDRegion.id]['confirmed_cases'] / \
                                                                 p[d][self.COVIDRegion.id]['total_tested']
            p[d]['testDate'] = p[d][self.COVIDRegion.id]['testDate']
        return p
