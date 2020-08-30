from datetime import datetime
from . import Snapshot

class StaffSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)

    def status(self):
        data = {
            'district_id': self.dc.district.id,
            'district_name': self.dc.district.name,
            'update_date': datetime.today(),
            'status': True,
            'facilities': [],
            'configuration': self.dc.configuration
        }

        for f in sorted(self.dc.facilities.values(), key=lambda x: x.facility_name):
            r = {
                'facility': f.facility_name,
                'update_date': datetime.today(),
                'status': True,
                'roles': []
            }
            for i in [i for i in self.dc.statusdata if i.facility_id == f.id]:
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
