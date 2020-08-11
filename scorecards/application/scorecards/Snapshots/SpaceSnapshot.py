from datetime import datetime
from .Snapshot import Snapshot

class SpaceSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)
        self.base_data=self.dc.base_data['space']

    def status(self):
        data = {
            'district_id': self.district.id,
            'update_date': datetime.today(),
            'status': True,
            'facilities': []
        }

        for f in self.base_data['facilities']:
            r={
                'facility': f['facility'],
                'update_date': datetime.today(),
                'status': True,
                'rooms': []
            }
            for i in [i for i in self.dc.statusdata if i.facility_name == f['facility']]:
                t = {
                    'room_type': i.description,
                    'capacity': i.available,
                    'demand': i.required,
                    'fill_pct': i.required / i.available,
                    'status': (i.required < i.available)
                }
                r['rooms'].append(t)
                if not t['status']:
                    r['status'] = False

            data['facilities'].append(r)
            if not r['status']:
                data['status'] = False

        return data
