from .DistrictDataCache import DistrictDataCache
from .PPEDataCache import PPEDataCache
from .StaffDataCache import StaffDataCache
from .SpaceDataCache import SpaceDataCache
from .TransDataCache import TransDataCache
from .GeoDataCache import GeoDataCache

class SummaryDataCache(DistrictDataCache):

    def __init__(self, district_id='3404906700000', dc=None):
        if dc is not None:
            super().__init__(dc=dc)
        else:
            super().__init__(district_id=district_id)

        self.dcs = {}
        self.dcs['ppe'] = PPEDataCache(dc=self)
        self.dcs['staff'] = StaffDataCache(dc=self)
        self.dcs['space'] = SpaceDataCache(dc=self)
        self.dcs['trans'] = TransDataCache(dc=self)
        self.dcs['geo'] = GeoDataCache(dc=self)
