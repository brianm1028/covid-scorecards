from datetime import datetime
import json
from ..Snapshot import Snapshot

# TODO implement StaffSnapshot class
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

            for role in f['roles']:
                t = {
                    'role_type': role['role_type'],
                    'required': role['required'],
                    'available': role['available'],
                    'substitutes': role['substitutes'],
                    'status': (role['available'] + role['substitutes'] - role['required'] > 0)
                }
                r['roles'].append(t)
                if not t['status']:
                    r['status'] = False

            data['facilities'].append(r)
            if not r['status']:
                data['status'] = False

        return data
