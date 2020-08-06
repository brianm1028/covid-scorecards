import requests
import json
from datetime import datetime, timedelta


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
