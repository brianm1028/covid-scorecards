from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

now = datetime.now()

app = Flask(__name__)

class District:
    lookup = {
        '115':
            {
                'zip_codes': ['60044', '60045'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '67':
            {
                'zip_codes': ['60045'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '65':
            {
                'zip_codes': ['60044'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '76':
            {
                'zip_codes': ['60060'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            }
    }

    def __init__(self, district):
        self.id = district
        self.zip_codes = District.lookup[district]['zip_codes']
        self.COVIDRegion = District.lookup[district]['COVIDRegion']
        self.counties = District.lookup[district]['counties']

class SnapshotSummary:

    def __init__(self, district):
        self.district_id = district.id
        self.ppe = PPESnapshot()
        self.staff = StaffSnapshot()
        self.trans = TransSnapshot()
        self.geo = GeoSnapshot(district)
        self.overall = Snapshot()
        self.overall.status = self.ppe.status and \
                              self.staff.status and \
                              self.trans.status and \
                              self.geo.status

class Snapshot:

    def __init__(self):
        self.status = 0

class PPESnapshot(Snapshot):
    pass

class StaffSnapshot(Snapshot):
    pass

class TransSnapshot(Snapshot):
    pass

def date_in_window(dv, td):
    d = datetime.strptime(dv, '%m/%d/%Y')
    return (d <= datetime.today()) and (d >= (datetime.today()-td))

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


class GeoSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district
        risk_metrics(self.district)

    def zip_positivity_rate(self):
        pass

    def county_positivity_rate(self):
        pass

    def region_positivity_rate(self):
        pass

    pass

@app.route('/status')
def status():
    return 'Online'

@app.route('/snapshot/<district_id>')
def get_overall_snapshot(district_id):
    snap = SnapshotSummary(District(district_id))
    return render_template('overall_snapshot.html', snap=snap)

@app.route('/snapshot/ppe/<district_id>')
def get_ppe_snapshot(district_id):
    snap = PPESnapshot(District(district_id))
    return render_template('ppe_snapshot.html', snap)

@app.route('/snapshot/staff/<district_id>')
def get_staff_snapshot(district_id):
    snap = StaffSnapshot(District(district_id))
    return render_template('staff_snapshot.html', snap)

@app.route('/snapshot/trans/<district_id>')
def get_trans_snapshot(district_id):
    snap = TransSnapshot(District(district_id))
    return render_template('trans_snapshot.html', snap)

@app.route('/snapshot/geo/<district_id>')
def get_geo_snapshot(district_id):
    snap = GeoSnapshot(District(district_id))
    return render_template('geo_snapshot.html', snap)


if __name__ == '__main__':
    app.run()
