# TODO add class documentation to District class
class District:
    # TODO move hard coded lookup table to a database
    lookup = {
        '115':
            {
                'zip_codes': ['60044', '60045'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '67':
            {
                'zip_codes': ['60045'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '65':
            {
                'zip_codes': ['60044'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            },
        '76':
            {
                'zip_codes': ['60060'],
                'COVIDRegion': 9,
                'counties': ['Lake', 'McHenry']
            }
    }

    def __init__(self, district):
        self.id = district
        self.zip_codes = District.lookup[district]['zip_codes']
        self.COVIDRegion = District.lookup[district]['COVIDRegion']
        self.counties = District.lookup[district]['counties']
