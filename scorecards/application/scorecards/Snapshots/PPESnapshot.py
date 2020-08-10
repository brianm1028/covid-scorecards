import json
from datetime import datetime
from . import Snapshot

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
            for i in [i for i in self.dc.inventory if i.facility_name == f['facility']]:
                t = {
                    'ppe_type': i.description,
                    'inventory': i.quantity,
                    'demand7': i.demand7,
                    'demand14': i.demand14,
                    'fullstock': (i.demand14 < i.quantity),
                    'status': (i.demand7 < i.quantity)
                }
                r['ppe_types'].append(t)
                if not t['status']:
                    r['status'] = False
            data['facilities'].append(r)
            if not r['status']:
                data['status'] = False

        return data
