from .DistrictDataCache import DistrictDataCache
from covidmetrics.application.models import PPEInventoryView

class PPEDataCache(DistrictDataCache):

    def __init__(self, district_id='3404906700000', dc=None):
        if dc is not None:
            super().__init__(dc=dc)
        else:
            super().__init__(district_id=district_id)

        #print(self.district)
        #print(self.facilities)
        #print(self.counties)
        #print(self.zip_codes)
        #print(self.COVIDRegion)

        self.inventory = PPEInventoryView.query.all()
