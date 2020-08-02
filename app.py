from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# TODO move Snapshot classes to a python package

# TODO add class documentation to District class
class District:
    # TODO move hard coded lookup table to a database
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

# TODO add class documentation to SnapshotSummary class
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
# TODO add class documentation to Snapshot class
class Snapshot:

    def __init__(self):
        self.status = 0

# TODO implement PPESnapshot class
class PPESnapshot(Snapshot):
    pass

# TODO implement StaffSnapshot class
class StaffSnapshot(Snapshot):
    pass

# TODO implement TransSnapshot class
class TransSnapshot(Snapshot):
    pass

# TODO move to a utility function library
def date_in_window(dv, td):
    d = datetime.strptime(dv, '%m/%d/%Y')
    return (d <= datetime.today()) and (d >= (datetime.today()-td))

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
        risk_metrics(self.district)
        self.status = 0

    def zip_positivity_rate(self):
        # TODO implement zip_code positivity rate calculation
        pass

    def county_positivity_rate(self):
        # TODO implement county positivity rate calculation
        pass

    def region_positivity_rate(self):
        # TODO implement region positivity rate calculation
        pass

@app.route('/status')
def status():
    return 'Online'

@app.route('/snapshot/<district_id>')
def get_overall_snapshot(district_id):
    snap = SnapshotSummary(District(district_id))
    return render_template('overall_snapshot.html', snap=snap)

# TODO consolidate get_<type>_snapshot methods using path parameter
# TODO implement SnapshotFactory class
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

# TODO create flask methods to support PPE inventory functions
# TODO create flask methods to support staff inventory functions
# TODO create flask methods to generate trend analysis views

if __name__ == '__main__':
    app.run()
