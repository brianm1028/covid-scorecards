from datetime import datetime
from .Snapshot import Snapshot

# TODO implement TransSnapshot class
class TransSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)

    def status(self):
        data = {
            'district_id': self.dc.district.id,
            'update_date': datetime.today(),
            'status': True
        }

        data['buses'] = {
                'update_date': datetime.today(),
                'status': True,
                'bus_groups': []
            }
        for g in [bg for bg in self.dc.bus_groups if bg.district_id == self.dc.district.id]:
            r = {
                'bus_group': g.description,
                'available': g.available,
                'required': g.required,
                'pct_avail': 1 - (g.required / g.available),
                'status': (g.required < g.available)
            }
            data['buses']['bus_groups'].append(r)
            if not r['status']:
                data['buses']['status'] = False

        if not data['buses']['status']:
            data['status'] = False

        return data
