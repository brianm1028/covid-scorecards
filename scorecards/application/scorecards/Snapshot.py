from datetime import datetime

# TODO add class documentation to Snapshot class
class Snapshot:

    def __init__(self, district):
        self.district = district

    def status(self):
        data = {
            'update_date': datetime.today(),
            'status': False,
        }
        return data
