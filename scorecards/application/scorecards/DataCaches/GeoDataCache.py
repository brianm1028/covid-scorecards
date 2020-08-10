from . import DataCache
import requests
from datetime import datetime, timedelta


def date_str(d=0):
    td = timedelta(days=d)
    d = datetime.today() - td
    s = '{mon}/{day}/{yr}'.format(day=d.day,mon=d.month,yr=d.year)
    return s


def date_in_window(dv, td):
    d = datetime.strptime(dv, '%m/%d/%Y')
    return (d <= datetime.today()) and (d >= (datetime.today() - td))


class GeoDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)

        self.county_list = self.load_county_list()
        self.covid_historical_test_results = self.load_covid_hist_test_data()
        self.covid_zip = self.load_covid_zip_data()

        self.zip_positivity = self.calculate_zip_positivity()
        self.county_positivity = self.calculate_county_positivity()
        self.region_positivity = self.calculate_region_positivity()

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

    def calculate_zip_positivity(self, days=3):
        data = {}
        for d in range(days+1):
            data[d] = {}
            for dv in [r for r in self.covid_zip['historical_zip']['values'] if r['testDate'] == date_str(d)]:
                for zv in [z for z in dv['values'] if z['zip'] in self.district.zip_codes]:
                    data[d][zv['zip']] = {
                        'confirmed_cases': zv['confirmed_cases'],
                        'total_tested': zv['total_tested'],
                        'testDate': dv['testDate']
                    }
        p = {}
        for d in range(days):
            p[d] = {}
            for z in self.district.zip_codes:
                p[d][z] = {
                    'confirmed_cases': (data[d][z]['confirmed_cases']-data[d+1][z]['confirmed_cases']),
                    'total_tested': (data[d][z]['total_tested']-data[d+1][z]['total_tested']),
                    'testDate': data[d][z]['testDate']
                }
                if p[d][z]['total_tested'] > 0:
                    p[d][z]['positivity_rate'] = p[d][z]['confirmed_cases'] / p[d][z]['total_tested']
                else:
                    p[d][z]['positivity_rate'] = 0
                p[d]['testDate'] = p[d][z]['testDate']
        print(p)
        return p

    def calculate_county_positivity(self, days=3):
        data = {}
        for d in range(days+1):
            data[d] = {}
            for dv in [r for r in self.covid_historical_test_results['historical_county']['values']
                       if r['testDate'] == date_str(d+3)]:
                for cv in [c for c in dv['values'] if c['County'] in self.district.counties]:
                    data[d][cv['County']] = {
                        'confirmed_cases': cv['confirmed_cases'],
                        'total_tested': cv['total_tested'],
                        'testDate': dv['testDate']
                    }

        p = {}
        for d in range(days):
            p[d] = {}
            for c in self.district.counties:
                p[d][c] = {
                    'confirmed_cases': (data[d][c]['confirmed_cases']-data[d+1][c]['confirmed_cases']),
                    'total_tested': (data[d][c]['total_tested']-data[d+1][c]['total_tested']),
                    'testDate': data[d][c]['testDate']
                }
                p[d][c]['positivity_rate'] = p[d][c]['confirmed_cases'] / p[d][c]['total_tested']
                p[d]['testDate'] = p[d][c]['testDate']
        print(p)
        return p

    def calculate_region_positivity(self, days=3):
        p = {}
        for d in range(days):
            p[d] = {}
            p[d][self.district.COVIDRegion] = {
                'confirmed_cases': 0,
                'total_tested': 0,
                'testDate': ''
            }
            for c in self.district.counties:
                p[d][self.district.COVIDRegion]['confirmed_cases'] += self.county_positivity[d][c]['confirmed_cases']
                p[d][self.district.COVIDRegion]['total_tested'] += self.county_positivity[d][c]['total_tested']
                p[d][self.district.COVIDRegion]['testDate'] = self.county_positivity[d][c]['testDate']
            p[d][self.district.COVIDRegion]['positivity_rate'] = p[d][self.district.COVIDRegion]['confirmed_cases'] / \
                                                                 p[d][self.district.COVIDRegion]['total_tested']
            p[d]['testDate'] = p[d][self.district.COVIDRegion]['testDate']
        print(p)
        return p
