from covidmetrics.application.models import DistrictView

class IndexDataCache:

    def __init__(self):
        self.districts = DistrictView.query.all()
