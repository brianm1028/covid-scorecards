from .DistrictDataCache import DistrictDataCache
from covidmetrics.application.models import StaffStatusView

class StaffDataCache(DistrictDataCache):

    def __init__(self, district_id='3404906700000', dc=None):
        if dc is not None:
            super().__init__(dc=dc)
        else:
            super().__init__(district_id=district_id)

        self.statusdata = StaffStatusView.query.all()