from datetime import datetime
from .Snapshot import Snapshot

# TODO implement TransSnapshot class
class TransSnapshot(Snapshot):

    def __init__(self, dc):
        super().__init__(dc)
        self.base_data=self.dc.base_data['trans']

    def status(self):
        data = {
            'district_id': self.district.id,
            'update_date': datetime.today(),
            'status': True
        }

        data['buses'] = {
                'update_date': datetime.today(),
                'status': True,
                'bus_groups': []
            }

        for g in self.base_data['bus_groups']:
            r = {
                'bus_group': g['group_name'],
                'available': g['bus_count']*g['seats_per_bus'],
                'required': 0,
                'pct_avail': 1-(0/(g['bus_count']*g['seats_per_bus'])),
                'status': (0 < (g['bus_count']*g['seats_per_bus']))
            }
            data['buses']['bus_groups'].append(r)
            if not r['status']:
                data['buses']['status'] = False

        if not data['buses']['status']:
            data['status'] = False

        return data
