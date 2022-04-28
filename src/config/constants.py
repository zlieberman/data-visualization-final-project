import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/unemployment.csv"
PROCESSED_DATA_FILE = "data/visualization_inputs/unemployment_input.csv"
NODES_FILE = 'data/connections/top5Manufacturing.csv'
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)
OUTPUT_HTML_PATH = os.path.join(ROOT_PATH, 'output')
NODES_FILE_PATH = os.path.join(ROOT_PATH, NODES_FILE)

# user controlled to determine how the data is visualized
PLOT_TYPE = 'USA-states' # 'country names', 'scatter'
DATA_INTERPRETATION = 'real values' # 'percent change'

# preproccessing constants
WTO_TO_GEOPANDAS_COUNTRY_NAMES = {
    'Russian Federation': 'Russia',
    'Saudi Arabia, Kingdom of': 'Saudi Arabia',
    'North Macedonia': 'Macedonia',
    'Czech Republic': 'Czechia',
    'Slovak Republic': 'Slovakia',
    'Brunei Darussalam': 'Brunei',
    'Moldova, Republic of': 'Moldova',
    'Korea, Republic of': 'South Korea',
    'Kuwait, the State of': 'Kuwait',
    'Venezuela, Bolivarian Republic of': 'Venezuela',
    'Bolivia, Plurinational State of': 'Bolivia',
    'Central African Republic': 'Central African Rep.',
    'Dominican Republic': 'Dominican Rep.',
}

US_STATE_TO_ABREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
}


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)