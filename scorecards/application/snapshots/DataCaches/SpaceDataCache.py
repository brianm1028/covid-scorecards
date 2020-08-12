from . import DataCache
from ...models import SpaceStatusView

class SpaceDataCache(DataCache):

    def __init__(self, district):
        super().__init__(district)
        self.statusdata = SpaceStatusView.query.all()
