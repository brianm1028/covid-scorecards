from datetime import datetime, timedelta
import requests
import json
from ..Snapshot import Snapshot

from ..DataCache import DataCache

# TODO add GeoSnapshot classs documentation
class GeoSnapshot(Snapshot):

    def __init__(self, district):
        super().__init__(district)
        self.base_data=self.dc.base_data['geo']


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
                'day1':self.dc.zip_positivity[0][z['zip_code']]['positivity_rate'],
                'day1date':self.dc.zip_positivity[0][z['zip_code']]['testDate'],
                'day2':self.dc.zip_positivity[1][z['zip_code']]['positivity_rate'],
                'day2date':self.dc.zip_positivity[1][z['zip_code']]['testDate'],
                'day3':self.dc.zip_positivity[2][z['zip_code']]['positivity_rate'],
                'day3date': self.dc.zip_positivity[2][z['zip_code']]['testDate']
            }
            r['status']= ((r['day1'] < z['threshold']) and
                          (r['day2'] < z['threshold']) and
                          (r['day3'] < z['threshold']))
            data['zip_data']['zip_codes'].append(r)
            data['zip_data']['day1date'] = self.dc.zip_positivity[0]['testDate']
            data['zip_data']['day2date'] = self.dc.zip_positivity[1]['testDate']
            data['zip_data']['day3date'] = self.dc.zip_positivity[2]['testDate']
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
                'day1':self.dc.county_positivity[0][c['county']]['positivity_rate'],
                'day2':self.dc.county_positivity[1][c['county']]['positivity_rate'],
                'day3':self.dc.county_positivity[2][c['county']]['positivity_rate']
                }
            r['status']= ((r['day1'] < c['threshold']) and
                           (r['day2'] < c['threshold']) and
                           (r['day3'] < c['threshold']))
            data['county_data']['counties'].append(r)
            data['county_data']['day1date'] = self.dc.county_positivity[0]['testDate']
            data['county_data']['day2date'] = self.dc.county_positivity[1]['testDate']
            data['county_data']['day3date'] = self.dc.county_positivity[2]['testDate']
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
                'day1': self.dc.region_positivity[0][g['region']]['positivity_rate'],
                'day2': self.dc.region_positivity[1][g['region']]['positivity_rate'],
                'day3': self.dc.region_positivity[2][g['region']]['positivity_rate']
                }
            r['status'] =  ((r['day1'] < g['threshold']) and
                           (r['day1'] < g['threshold']) and
                           (r['day1'] < g['threshold']))
            data['region_data']['regions'].append(r)
            data['region_data']['day1date'] = self.dc.region_positivity[0]['testDate']
            data['region_data']['day2date'] = self.dc.region_positivity[1]['testDate']
            data['region_data']['day3date'] = self.dc.region_positivity[2]['testDate']
            if not r['status']:
                data['region_data']['status'] = False

        if not data['region_data']['status']:
            data['status'] = False

        return data
