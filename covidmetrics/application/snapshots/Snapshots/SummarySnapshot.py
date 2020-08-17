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
        self.dc = dc
        self.district_id = self.district.id
        if self.dc.configuration.config()["ppe"]["enabled"]:
            self.ppe = PPESnapshot(dc.dcs['ppe'])
        if self.dc.configuration.config()["staff"]["enabled"]:
            self.staff = StaffSnapshot(dc.dcs['staff'])
        if self.dc.configuration.config()["space"]["enabled"]:
            self.space = SpaceSnapshot(dc.dcs['space'])
        if self.dc.configuration.config()["trans"]["enabled"]:
            self.trans = TransSnapshot(dc.dcs['trans'])
        if self.dc.configuration.config()["geo"]["enabled"]:
            self.geo = GeoSnapshot(dc.dcs['geo'])

    def calc_status(self):

        status = True
        if self.dc.configuration.config()["ppe"]["enabled"]:
            status = (status and self.ppe.status()['status'])
        if self.dc.configuration.config()["staff"]["enabled"]:
            status = (status and self.staff.status()['status'])
        if self.dc.configuration.config()["space"]["enabled"]:
            status = (status and self.space.status()['status'])
        if self.dc.configuration.config()["trans"]["enabled"]:
            status = (status and self.trans.status()['status'])
        if self.dc.configuration.config()["geo"]["enabled"]:
            status = (status and self.geo.status()['status'])
        return status

    def status(self):
        data = {
            'district_id': self.district_id,
            'district_name': self.district.name,
            'update_data': datetime.today(),
            'status': self.calc_status(),
            'configuration': self.dc.configuration,
            'snapshots': {}
        }
        if self.dc.configuration.config()["ppe"]["enabled"]:
            data['snapshots']['ppe'] = self.ppe.status()
        if self.dc.configuration.config()["staff"]["enabled"]:
            data['snapshots']['staff'] = self.staff.status()
        if self.dc.configuration.config()["space"]["enabled"]:
            data['snapshots']['space'] = self.space.status()
        if self.dc.configuration.config()["trans"]["enabled"]:
            data['snapshots']['trans'] = self.trans.status()
        if self.dc.configuration.config()["geo"]["enabled"]:
            data['snapshots']['geo'] = self.geo.status()

        return data
