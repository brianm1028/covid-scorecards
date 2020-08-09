import json
from datetime import datetime
from ..Snapshot import Snapshot

class PPESnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)
        self.base_data=self.dc.base_data['ppe']

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
                'ppe_types': []
            }

            for ppe in f['ppe_types']:
                t = {
                    'ppe_type': ppe['ppe_type'],
                    'inventory': ppe['inventory'],
                    'demand7': ppe['demand7'],
                    'demand14': ppe['demand14'],
                    'fullstock': (ppe['demand14'] < ppe['inventory']),
                    'status': (ppe['demand7'] < ppe['inventory'])
                }
                r['ppe_types'].append(t)
                if not t['status']:
                    r['status'] = False

            data['facilities'].append(r)
            if not r['status']:
                data['status'] = False

        return data
