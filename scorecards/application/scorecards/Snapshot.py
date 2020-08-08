from datetime import datetime
from .DataCache import DataCache

# TODO add class documentation to Snapshot class
class Snapshot:

    def __init__(self, district):
        self.district = district
        self.dc = DataCache(district)

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': False,
        }
        return data
