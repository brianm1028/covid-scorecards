from . import DataCache
from ...models import StaffStatusView

class StaffDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)
        self.statusdata = StaffStatusView.query.all()