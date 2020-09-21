from datetime import datetime, timedelta
from . import Snapshot

# TODO add GeoSnapshot classs documentation
class GeoSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)


    def status(self):
        data = {
            'district_id': self.dc.district.id,
            'district_name': self.dc.district.name,
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
                'status': True,
                'inchybstatus': True,
                'incinpstatus': True,
                'clihybstatus': True,
                'cliinpstatus': True,
                'tathybstatus': True,
                'tatinpstatus': True
                }

            for d in range(self.dc.configuration.config()["geo"]["county_duration"]):
                r['day'+str(d)] = self.dc.county_positivity[d][c]['positivity_rate']
                if self.dc.county_positivity[d][c]['positivity_rate'] > self.dc.configuration.config()["geo"]["county_threshold"]:
                    r['status']=False
                data['county_data']['day'+str(d)+'date'] = self.dc.county_positivity[d]['testDate']
                if not r['status']:
                    data['county_data']['status'] = False

            for d in range(self.dc.configuration.config()["geo"]["county_inc_duration"]):
                r['day'+str(d)+'inc'] = self.dc.county_incidence[d][c]['dur_roll_avg_incidence']
                #TODO: add threshold to configuration for incidence rate
                if not (self.dc.county_incidence[d][c]['dur_roll_avg_incidence'] < self.dc.configuration.config()["geo"]["county_inc_hyb_threshold"]):
                    r['inchybstatus'] = False
                if not (self.dc.county_incidence[d][c]['dur_roll_avg_incidence'] < self.dc.configuration.config()["geo"]["county_inc_inp_threshold"]):
                    r['incinpstatus'] = False
                data['county_data']['day'+str(d)+'incdate'] = self.dc.county_incidence[d]['testDate']

            non_increasing=0
            for d in range(self.dc.configuration.config()["geo"]["county_cli_duration"]):
                if c in self.dc.cli_metrics[d].keys():
                    if self.dc.cli_metrics[d+1][c]['cli_admissions']<=self.dc.cli_metrics[d][c]['cli_admissions']:
                        non_increasing+=1
                    r['day'+str(d)+'cli'] = self.dc.cli_metrics[d][c]['cli_admissions']
                else:
                    non_increasing+=1
                    r['day'+str(d)+'cli'] = 0
                data['county_data']['day'+str(d)+'clidate'] = self.dc.cli_metrics[d]['testDate']
            if non_increasing <= self.dc.configuration.config()["geo"]["county_cli_hyb_threshold"]:
                r['clihybstatus'] = False
            if non_increasing <= self.dc.configuration.config()["geo"]["county_cli_inp_threshold"]:
                r['cliinpstatus'] = False

            print(self.dc.configuration.config())
            for d in range(self.dc.configuration.config()["geo"]["county_tat_duration"]):
                print(d)
                print(self.dc.tat_metrics)
                if c in self.dc.tat_metrics[d].keys():
                    print(c)
                    r['day'+str(d)+'tat'] = self.dc.tat_metrics[d][c]['tat_days']
                    if not (self.dc.tat_metrics[d][c]['tat_days'] < self.dc.configuration.config()["geo"]["county_tat_hyb_threshold"]):
                        r['tathybstatus'] = False
                    if not (self.dc.tat_metrics[d][c]['tat_days'] < self.dc.configuration.config()["geo"]["county_tat_inp_threshold"]):
                        r['tatinpstatus'] = False
                else:
                    r['day' + str(d) + 'tat'] = 0
                data['county_data']['day'+str(d)+'tatdate'] = self.dc.tat_metrics[d]['testDate']

            if not r['inchybstatus'] or not r['clihybstatus'] or not r['tathybstatus']:
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
            if self.dc.region_positivity[d][self.dc.COVIDRegion.id]['positivity_rate'] > self.dc.configuration.config()["geo"]["region_threshold"]:
                r['status']=False
            data['region_data']['day'+str(d)+'date'] = self.dc.region_positivity[d][self.dc.COVIDRegion.id]['testDate']
            if not r['status']:
                data['region_data']['status'] = False

        data['region_data']['regions'].append(r)

        if not data['region_data']['status']:
            data['status'] = False
        print(data)
        return data
