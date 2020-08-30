from covidmetrics.application.models import DistrictView
from ..models import District

class IndexDataCache:

    def __init__(self):
        self.districts = sorted(District.query.all(), key=lambda x: x.district_code)

