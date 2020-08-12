from datetime import datetime
from . import Snapshot

class StaffSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)
        self.base_data=self.dc.base_data['staff']

    def status(self):
        data = {
            'district_id': self.district.id,
            'update_date': datetime.today(),
            'status': True,
            'facilities': []
        }

        for f in self.base_data['facilities']:
            r = {
                'facility': f['facility'],
                'update_date': datetime.today(),
                'status': True,
                'roles': []
            }
            for i in [i for i in self.dc.statusdata if i.facility_name == f['facility']]:
                t = {
                    'role_type': i.role_type,
                    'required': i.required,
                    'available': i.available,
                    'status': (i.available >= i.required)
                }
                r['roles'].append(t)
                if not t['status']:
                    r['status'] = False

            data['facilities'].append(r)
            if not r['status']:
                data['status'] = False

        return data
