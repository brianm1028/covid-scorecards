from datetime import datetime
from .Snapshot import Snapshot

class SpaceSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)

    def status(self):
        data = {
            'district_id': self.dc.district.id,
            'update_date': datetime.today(),
            'status': True,
            'facilities': []
        }

        for f in self.dc.facilities.values():
            r={
                'facility': f.facility_name,
                'update_date': datetime.today(),
                'status': True,
                'rooms': []
            }
            for i in [i for i in self.dc.statusdata if i.facility_name == f.id]:
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
