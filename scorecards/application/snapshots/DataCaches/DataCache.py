import json

class DataCache:

    def __init__(self, district):
        self.district = district
        with open('data/base_data.json') as f:
            self.base_data = json.load(f)[district.id]
