from datetime import datetime
from .PPESnapshot import PPESnapshot
from .StaffSnapshot import StaffSnapshot
from .SpaceSnapshot import SpaceSnapshot
from .TransSnapshot import TransSnapshot
from .GeoSnapshot import GeoSnapshot


# TODO add class documentation to SnapshotSummary class
class SummarySnapshot:

    def __init__(self, dc):
        self.district=dc.district
        self.district_id = self.district.id
        self.ppe = PPESnapshot(dc.dcs['ppe'])
        self.staff = StaffSnapshot(dc.dcs['staff'])
        self.space = SpaceSnapshot(dc.dcs['space'])
        self.trans = TransSnapshot(dc.dcs['trans'])
        self.geo = GeoSnapshot(dc.dcs['geo'])

    def calc_status(self):
        status = self.ppe.status()['status'] and \
               self.staff.status()['status'] and \
               self.space.status()['status'] and \
               self.trans.status()['status'] and \
               self.geo.status()['status']
        return status

    def status(self):
        data = {
            'district_id': self.district_id,
            'update_data': datetime.today(),
            'status': self.calc_status(),
            'snapshots': {
                'ppe': self.ppe.status(),
                'staff': self.staff.status(),
                'space': self.space.status(),
                'trans': self.trans.status(),
                'geo': self.geo.status()
            }
        }
        return data
