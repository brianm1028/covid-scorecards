from datetime import datetime
from .DataCache import DataCache

# TODO add class documentation to Snapshot class
class Snapshot:

    def __init__(self, dc):
        self.district = dc.district
        self.dc = dc

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': False,
        }
        return data
