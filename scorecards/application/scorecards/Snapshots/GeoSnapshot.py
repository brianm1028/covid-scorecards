from datetime import datetime, timedelta
import requests
import json
from ..Snapshot import Snapshot


# TODO move to a utility function library
def date_in_window(dv, td):
    d = datetime.strptime(dv, '%m/%d/%Y')
    return (d <= datetime.today()) and (d >= (datetime.today() - td))


# TODO replace county_historical by moving into risk_metrics
def county_historical(district):
    r = requests.get('https://www.dph.illinois.gov/sitefiles/COVIDHistoricalTestResults.json?nocache=1')
    county_history = r.json()['historical_county']

    data = []
    d = [r for r in county_history['values'] if date_in_window(r['testDate'], timedelta(days=7))]
    for r in d:
        data.append({
            'testDate': r['testDate'],
            'values': [s for s in r['values'] if s['County'] in district.counties]
        })
    print(data)


# TODO move risk_metrics to static object methods
def risk_metrics(district):
    r = requests.get('https://www.dph.illinois.gov/sitefiles/COVIDCountyRiskMetrics.json?nocache=1')
    tp = r.json()['testPositivity']

    data = []
    d = [r for r in tp if date_in_window(r['report_date'], timedelta(days=7))]
    for r in d:
        data.append({
            'report_date': r['report_date'],
            'values': [s for s in r['values'] if s['County'] in district.counties]
        })
    print(data)


# TODO add GeoSnapshot classs documentation
class GeoSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district
        with open('data/base_data.json') as f:
            self.base_data = json.load(f)[self.district.id]['geo']

    def status(self):
        data = {
            'district_id': self.district.id,
            'update_date': datetime.today(),
            'status': True,
        }

        data['zip_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'zip_codes': []
        }

        for z in self.base_data['zip_codes']:
            r = {
                'zip_code': z['zip_code'],
                'population': z['population'],
                'new_cases': z['new_cases'],
                'cases_per_10k': z['new_cases'] * 10000 / z['population'],
                'status': (z['new_cases'] * 10000 / z['population'] < z['threshold'])
            }
            data['zip_data']['zip_codes'].append(r)
            if not r['status']:
                data['zip_data']['status'] = False


        if not data['zip_data']['status']:
            data['status'] = False

        data['county_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'counties': []
        }

        for c in self.base_data['counties']:
            r = {
                'county': c['county'],
                'total_tests': c['total_tests'],
                'positive_tests': c['positive_tests'],
                'positivity_rate': c['positive_tests']/c['total_tests'],
                'status': (c['positive_tests']/c['total_tests'] < c['threshold'])
            }
            data['county_data']['counties'].append(r)
            if not r['status']:
                data['county_data']['status'] = False

        if not data['county_data']['status']:
            data['status'] = False



        data['region_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'regions': []
        }

        for g in self.base_data['regions']:
            r = {
                'region': g['region'],
                'total_tests': g['total_tests'],
                'positive_tests': g['positive_tests'],
                'positivity_rate': g['positive_tests']/g['total_tests'],
                'status': (g['positive_tests']/g['total_tests'] < g['threshold'])
            }
            data['region_data']['regions'].append(r)
            if not r['status']:
                data['region_data']['status'] = False

        if not data['region_data']['status']:
            data['status'] = False

        return data

    def zip_positivity_rate(self):
        # TODO implement zip_code positivity rate calculation
        pass

    def county_positivity_rate(self):
        # TODO implement county positivity rate calculation
        pass

    def region_positivity_rate(self):
        # TODO implement region positivity rate calculation
        pass
