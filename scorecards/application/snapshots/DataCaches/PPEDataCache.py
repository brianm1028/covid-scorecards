from . import DataCache
from ...models import PPEInventoryView

class PPEDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)
        self.inventory = PPEInventoryView.query.all()
