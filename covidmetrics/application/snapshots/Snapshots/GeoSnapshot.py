from datetime import datetime, timedelta
from . import Snapshot

# TODO add GeoSnapshot classs documentation
class GeoSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)


    def status(self):
        data = {
            'district_id': self.dc.district.id,
            'update_date': datetime.today(),
            'status': True,
            'configuration': self.dc.configuration
        }

        data['zip_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'zip_codes': []
        }

        for z in self.dc.zip_codes:
            r = {
                'zip_code': z,
                'status': True
            }
            for d in range(self.dc.configuration.config()["geo"]["zip_duration"]):
                r['day'+str(d)] = self.dc.zip_positivity[d][z]['positivity_rate']
                r['status'] = (self.dc.zip_positivity[d][z]['positivity_rate'] < self.dc.configuration.config()["geo"]["zip_threshold"])
                data['zip_data']['day' + str(d) + 'date'] = self.dc.zip_positivity[d]['testDate']
                if not r['status']:
                    data['zip_data']['status'] = False
            data['zip_data']['zip_codes'].append(r)

        if not data['zip_data']['status']:
            data['status'] = False

        data['county_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'counties': []
        }

        for c in self.dc.counties:
            r = {
                'county': c,
                'status': True
                }
            for d in range(self.dc.configuration.config()["geo"]["county_duration"]):
                r['day'+str(d)] = self.dc.county_positivity[d][c]['positivity_rate']
                r['status'] = (self.dc.county_positivity[d][c]['positivity_rate'] < self.dc.configuration.config()["geo"]["county_threshold"])
                data['county_data']['day'+str(d)+'date'] = self.dc.county_positivity[d]['testDate']
                if not r['status']:
                    data['county_data']['status'] = False
            data['county_data']['counties'].append(r)

        if not data['county_data']['status']:
            data['status'] = False

        data['region_data'] = {
            'update_date': datetime.today(),
            'status': True,
            'regions': []
        }

        r = {
            'region': self.dc.COVIDRegion.id,
            'status': True
            }
        for d in range(self.dc.configuration.config()["geo"]["region_duration"]):
            r['day' + str(d)] = self.dc.region_positivity[d][self.dc.COVIDRegion.id]['positivity_rate']
            r['status'] = (self.dc.region_positivity[d][self.dc.COVIDRegion.id]['positivity_rate'] < self.dc.configuration.config()["geo"]["region_threshold"])
            data['region_data']['day'+str(d)+'date'] = self.dc.region_positivity[d][self.dc.COVIDRegion.id]['testDate']
            if not r['status']:
                data['region_data']['status'] = False

        data['region_data']['regions'].append(r)

        if not data['region_data']['status']:
            data['status'] = False
        print(data)
        return data
