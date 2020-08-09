from datetime import datetime
from .Snapshots import PPESnapshot, StaffSnapshot, SpaceSnapshot, TransSnapshot, GeoSnapshot

# TODO add class documentation to SnapshotSummary class
class SnapshotSummary:

    def __init__(self, dc):
        self.district=dc.district
        self.district_id = self.district.id
        self.ppe = PPESnapshot(dc)
        self.staff = StaffSnapshot(dc)
        self.space = SpaceSnapshot(dc)
        self.trans = TransSnapshot(dc)
        self.geo = GeoSnapshot(dc)

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
