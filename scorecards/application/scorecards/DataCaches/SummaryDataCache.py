from . import DataCache
from .PPEDataCache import PPEDataCache
from .StaffDataCache import StaffDataCache
from .SpaceDataCache import SpaceDataCache
from .TransDataCache import TransDataCache
from .GeoDataCache import GeoDataCache

class SummaryDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)
        self.dcs = {}
        self.dcs['ppe'] = PPEDataCache(district)
        self.dcs['staff'] = StaffDataCache(district)
        self.dcs['space'] = SpaceDataCache(district)
        self.dcs['trans'] = TransDataCache(district)
        self.dcs['geo'] = GeoDataCache(district)
