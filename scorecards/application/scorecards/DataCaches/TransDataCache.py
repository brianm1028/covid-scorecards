from . import DataCache
from ...models import BusGroup

class TransDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)
        self.bus_groups = BusGroup.query.all()
        print(self.bus_groups)
