from ..models import District
from ..models import Facility
from ..models import County
from ..models import COVIDRegion
from ..models import ZipCode
from ..models import Configuration

class DistrictDataCache():

    def __init__(self,district_id='3404906700000', dc=None):
        if dc is not None:
            self.district = dc.district
            self.configuration = dc.configuration
            self.facilities = dc.facilities
            self.counties = dc.counties
            self.zip_codes = dc.zip_codes
            self.COVIDRegion = dc.COVIDRegion
        else:
            self.district = District.query.get([district_id])
            self.configuration = Configuration.query.get([district_id])
            self.facilities={}
            self.counties={}
            self.zip_codes={}

            self.zip_codes[self.district.base_zip_code] = ZipCode.query.get([self.district.base_zip_code])
            self.counties[self.district.county_name] = County.query.get([self.district.county_name])
            self.COVIDRegion = COVIDRegion.query.get([self.counties[self.district.county_name].COVIDRegion])

            for f in Facility.query.filter(Facility.district_id==self.district.id).all():
                self.facilities[f.id]=f
                if f.zip_code not in self.zip_codes.keys():
                    self.zip_codes[f.zip_code]=ZipCode.query.get([f.zip_code])

            for c in County.query.filter(County.COVIDRegion==self.COVIDRegion.id).all():
                if c.name not in self.counties.keys():
                    self.counties[c.name]=County.query.get([c.name])

        print(self)

