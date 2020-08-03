import requests
from datetime import datetime, timedelta


# TODO add class documentation to SnapshotSummary class
class SnapshotSummary:

    def __init__(self, district):
        self.district_id = district.id
        self.ppe = PPESnapshot(district)
        self.staff = StaffSnapshot(district)
        self.space = SpaceSnapshot(district)
        self.trans = TransSnapshot(district)
        self.geo = GeoSnapshot(district)

    def calc_status(self):
        status = self.ppe.status()['status'] and \
               self.staff.status()['status'] and \
               self.space.status()['status'] and \
               self.trans.status()['status'] and \
               self.geo.status()['status']
        return status

    def status(self):
        data = {
            'district_id': self.district_id,
            'update_data': datetime.today(),
            'status': self.calc_status(),
            'snapshots': {
                'ppe': self.ppe.status(),
                'staff': self.staff.status(),
                'space': self.space.status(),
                'trans': self.trans.status(),
                'geo': self.geo.status()
            }
        }
        return data

# TODO add class documentation to Snapshot class
class Snapshot:

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
        }
        return data

# TODO implement PPESnapshot class
class PPESnapshot(Snapshot):

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
            'facilities': [
                {
                    'facility': 'Cherokee',
                    'update_date': datetime.today(),
                    'status': 0,
                    'ppe_types': [
                        {
                            'ppe_type': 'Cloth Masks',
                            'inventory': 300,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (300 > 100)
                        },
                        {
                            'ppe_type': 'Paper Masks',
                            'inventory': 30,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (30 > 100)
                        }
                    ]
                },
                {
                    'facility': 'Everett',
                    'update_date': datetime.today(),
                    'status': 0,
                    'ppe_types': [
                        {
                            'ppe_type': 'Cloth Masks',
                            'inventory': 300,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (300 > 100)
                        },
                        {
                            'ppe_type': 'Paper Masks',
                            'inventory': 30,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (30 > 100)
                        }
                    ]
                },
                {
                    'facility': 'Sheridan',
                    'update_date': datetime.today(),
                    'status': 0,
                    'ppe_types': [
                        {
                            'ppe_type': 'Cloth Masks',
                            'inventory': 300,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (300 > 100)
                        },
                        {
                            'ppe_type': 'Paper Masks',
                            'inventory': 30,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (30 > 100)
                        }
                    ]
                },
                {
                    'facility': 'Deerpath',
                    'update_date': datetime.today(),
                    'status': 0,
                    'ppe_types': [
                        {
                            'ppe_type': 'Cloth Masks',
                            'inventory': 300,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (300 > 100)
                        },
                        {
                            'ppe_type': 'Paper Masks',
                            'inventory': 30,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (30 > 100)
                        }
                    ]
                },
                {
                    'facility': 'LFHS',
                    'update_date': datetime.today(),
                    'status': 0,
                    'ppe_types': [
                        {
                            'ppe_type': 'Cloth Masks',
                            'inventory': 300,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (300 > 100)
                        },
                        {
                            'ppe_type': 'Paper Masks',
                            'inventory': 30,
                            'demand7': 100,
                            'demand14': 200,
                            'status': (30 > 100)
                        }
                    ]
                }
            ]
        }
        return data


# TODO implement StaffSnapshot class
class StaffSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
            'facilities': [
                {
                    'facility': 'Cherokee',
                    'update_date': datetime.today(),
                    'status': 0,
                    'roles': [
                        {
                            'role_type': 'Certified Educator',
                            'required': 100,
                            'available': 105,
                            'substitutes': 2,
                            'status': (105 + 2 - 100 > 0)
                        },
                        {
                            'role_type': 'Admin and Facility Staff',
                            'required': 10,
                            'available': 11,
                            'substitutes': 0,
                            'status': (11 + 0 - 10 > 0)
                        }
                    ]
                },
                {
                    'facility': 'Everett',
                    'update_date': datetime.today(),
                    'status': 0,
                    'roles': [
                        {
                            'role_type': 'Certified Educator',
                            'required': 100,
                            'available': 105,
                            'substitutes': 2,
                            'status': (105 + 2 - 100 > 0)
                        },
                        {
                            'role_type': 'Admin and Facility Staff',
                            'required': 10,
                            'available': 11,
                            'substitutes': 0,
                            'status': (11 + 0 - 10 > 0)
                        }
                    ]
                },
                {
                    'facility': 'Sheridan',
                    'update_date': datetime.today(),
                    'status': 0,
                    'roles': [
                        {
                            'role_type': 'Certified Educator',
                            'required': 100,
                            'available': 105,
                            'substitutes': 2,
                            'status': (105 + 2 - 100 > 0)
                        },
                        {
                            'role_type': 'Admin and Facility Staff',
                            'required': 10,
                            'available': 11,
                            'substitutes': 0,
                            'status': (11 + 0 - 10 > 0)
                        }
                    ]
                },
                {
                    'facility': 'Deerpath',
                    'update_date': datetime.today(),
                    'status': 0,
                    'roles': [
                        {
                            'role_type': 'Certified Educator',
                            'required': 100,
                            'available': 105,
                            'substitutes': 2,
                            'status': (105 + 2 - 100 > 0)
                        },
                        {
                            'role_type': 'Admin and Facility Staff',
                            'required': 10,
                            'available': 11,
                            'substitutes': 0,
                            'status': (11 + 0 - 10 > 0)
                        }
                    ]
                },
                {
                    'facility': 'LFHS',
                    'update_date': datetime.today(),
                    'status': 0,
                    'roles': [
                        {
                            'role_type': 'Certified Educator',
                            'required': 100,
                            'available': 105,
                            'substitutes': 2,
                            'status': (105 + 2 - 100 > 0)
                        },
                        {
                            'role_type': 'Admin and Facility Staff',
                            'required': 10,
                            'available': 11,
                            'substitutes': 0,
                            'status': (11 + 0 - 10 > 0)
                        }
                    ]
                }
            ]
        }
        return data


# TODO implement SpaceSnapshot class
class SpaceSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
            'facilities': [
                {
                    'facility': 'Cherokee',
                    'update_date': datetime.today(),
                    'status': 0,
                    'rooms': [
                        {
                            'room_type': 'General Classroom',
                            'room_count': 30,
                            'avg_room_capacity': 10,
                            'capacity': 300,
                            'demand': 275,
                            'fill_pct': 300/275,
                            'avg_class': 275/10,
                            'status': (275 < 300)
                        },
                        {
                            'room_type': 'Special Classroom',
                            'room_count': 3,
                            'avg_room_capacity': 10,
                            'capacity': 30,
                            'demand': 40,
                            'fill_pct': 30 / 40,
                            'avg_class': 40 / 3,
                            'status': (40 < 30)
                        }

                    ]
                },
                {
                    'facility': 'Everett',
                    'update_date': datetime.today(),
                    'status': 0,
                    'rooms': [
                        {
                            'room_type': 'General Classroom',
                            'room_count': 30,
                            'avg_room_capacity': 10,
                            'capacity': 300,
                            'demand': 275,
                            'fill_pct': 300 / 275,
                            'avg_class': 275 / 10,
                            'status': (275 < 300)
                        },
                        {
                            'room_type': 'Special Classroom',
                            'room_count': 3,
                            'avg_room_capacity': 10,
                            'capacity': 30,
                            'demand': 40,
                            'fill_pct': 30 / 40,
                            'avg_class': 40 / 3,
                            'status': (40 < 30)
                        }

                    ]
                },
                {
                    'facility': 'Sheridan',
                    'update_date': datetime.today(),
                    'status': 0,
                    'rooms': [
                        {
                            'room_type': 'General Classroom',
                            'room_count': 30,
                            'avg_room_capacity': 10,
                            'capacity': 300,
                            'demand': 275,
                            'fill_pct': 300 / 275,
                            'avg_class': 275 / 10,
                            'status': (275 < 300)
                        },
                        {
                            'room_type': 'Special Classroom',
                            'room_count': 3,
                            'avg_room_capacity': 10,
                            'capacity': 30,
                            'demand': 40,
                            'fill_pct': 30 / 40,
                            'avg_class': 40 / 3,
                            'status': (40 < 30)
                        }

                    ]
                },
                {
                    'facility': 'Deerpath',
                    'update_date': datetime.today(),
                    'status': 0,
                    'rooms': [
                        {
                            'room_type': 'General Classroom',
                            'room_count': 30,
                            'avg_room_capacity': 10,
                            'capacity': 300,
                            'demand': 275,
                            'fill_pct': 300 / 275,
                            'avg_class': 275 / 10,
                            'status': (275 < 300)
                        },
                        {
                            'room_type': 'Special Classroom',
                            'room_count': 3,
                            'avg_room_capacity': 10,
                            'capacity': 30,
                            'demand': 40,
                            'fill_pct': 30 / 40,
                            'avg_class': 40 / 3,
                            'status': (40 < 30)
                        }

                    ]
                },
                {
                    'facility': 'LFHS',
                    'update_date': datetime.today(),
                    'status': 0,
                    'rooms': [
                        {
                            'room_type': 'General Classroom',
                            'room_count': 30,
                            'avg_room_capacity': 10,
                            'capacity': 300,
                            'demand': 275,
                            'fill_pct': 300 / 275,
                            'avg_class': 275 / 10,
                            'status': (275 < 300)
                        },
                        {
                            'room_type': 'Special Classroom',
                            'room_count': 3,
                            'avg_room_capacity': 10,
                            'capacity': 30,
                            'demand': 40,
                            'fill_pct': 30 / 40,
                            'avg_class': 40 / 3,
                            'status': (40 < 30)
                        }

                    ]
                }
            ]
        }
        return data


# TODO implement TransSnapshot class
class TransSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
            'buses': {
                'update_date': datetime.today(),
                'status': 0,
                'bus_groups': [
                    {
                        'bus_group': 'AM Elementary',
                        'available': 10,
                        'required': 9,
                        'pct_avail': 1-(9/10),
                        'status': (9 < 10)
                    },
                    {
                        'bus_group': 'PM Elementary',
                        'available': 5,
                        'required': 9,
                        'pct_avail': 1-(9/5),
                        'status': (9 < 5)
                    }
                ]
            },
            'drivers': {
                'update_date': datetime.today(),
                'status': 0,
                'bus_groups': [
                    {
                        'bus_group': 'AM Elementary',
                        'available': 10,
                        'required': 9,
                        'pct_avail': 1 - (9 / 10),
                        'status': (9 < 10)
                    },
                    {
                        'bus_group': 'PM Elementary',
                        'available': 5,
                        'required': 9,
                        'pct_avail': 1 - (9 / 5),
                        'status': (9 < 5)
                    }
                ]
            }

        }
        return data


# TODO add GeoSnapshot classs documentation
class GeoSnapshot(Snapshot):

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': 0,
            'zip_data': {
                'update_date': datetime.today(),
                'status': 0,
                'zip_codes': [
                    {
                        'zip_code': '60044',
                        'population': 12345,
                        'new_cases': 20,
                        'cases_per_10k': 10*10000/12345,
                        'status': (10*10000/12345 < 8)
                    },
                    {
                        'zip_code': '60045',
                        'population': 12345,
                        'new_cases': 2,
                        'cases_per_10k': 10 * 10000 / 12345,
                        'status': (10 * 10000 / 12345 < 8)
                    }
                ]
            },
            'county_data': {
                'update_date': datetime.today(),
                'status': 0,
                'counties': [
                    {
                        'county': 'Lake',
                        'total_tests': 12345,
                        'positive_tests': 20,
                        'positivity_rate': 20/12345,
                        'status': (20/12345 < .08)
                    },
                    {
                        'county': 'McHenry',
                        'total_tests': 234,
                        'positive_tests': 40,
                        'positivity_rate': 40 / 234,
                        'status': (20 / 12345 < .08)
                    }
                ]
            },
            'region_data': {
                'update_date': datetime.today(),
                'status': 0,
                'regions': [
                    {
                        'region': 9,
                        'total_tests': 12345,
                        'positive_tests': 20,
                        'positivity_rate': 20/12345,
                        'status': (20/12345 < .08)
                    },
                    {
                        'region': 99,
                        'total_tests': 234,
                        'positive_tests': 40,
                        'positivity_rate': 40 / 234,
                        'status': (40 / 234 < .08)
                    }
                ]
            }
        }
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
