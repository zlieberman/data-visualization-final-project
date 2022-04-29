import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/merged_gdp_gdpc_mortality.csv"
PROCESSED_DATA_FILE = "data/visualization_inputs/globalGDPInput.csv"
NODES_FILE = 'data/connections/top5Manufacturing.csv'
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)
OUTPUT_HTML_PATH = os.path.join(ROOT_PATH, 'output')
NODES_FILE_PATH = os.path.join(ROOT_PATH, NODES_FILE)

# user controlled to determine how the data is visualized
PLOT_TYPE = 'country names' # 'country names', 'scatter', 'USA-states'
DATA_INTERPRETATION = 'percent change' # 'percent change', 'real values'
PLOT_TITLE='COVID-19 spread across the USA'
COLORBAR_TITLE='Number of cases'

# preproccessing constants
DATASET1 = 'data/gdp-per-capita-maddison-2020.csv'
DATASET2 = 'data/child-mortality-igme.csv'
DATASET1_PATH = os.path.join(ROOT_PATH, DATASET1)
DATASET2_PATH = os.path.join(ROOT_PATH, DATASET2)
MERGED_FILE_PATH = os.path.join(ROOT_PATH, 'data/merged_gdp_mortality.csv')


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

USA_STATES_TO_REGION = {'AK': 'West', 'AL': 'South', 'AR': 'South',
    'AZ': 'West', 'CA': 'West', 'CO': 'West', 
    'CT': 'Northeast', 'DC': 'South', 'DE': 'South', 
    'FL': 'South', 'GA': 'South', 'HI': 'West', 
    'IA': 'Midwest', 'ID': 'West', 'IL': 'Midwest', 
    'IN': 'Midwest', 'KS': 'Midwest', 'KY': 'South', 
    'LA': 'South', 'MA': 'Northeast', 'MD': 'South', 
    'ME': 'Northeast', 'MI': 'Midwest', 'MN': 'Midwest',
    'MO': 'Midwest', 'MS': 'South', 'MT': 'West', 
    'NC': 'South', 'ND': 'Midwest', 'NE': 'Midwest', 
    'NH': 'Northeast', 'NJ': 'Northeast', 'NM': 'West', 
    'NV': 'West', 'NY': 'Northeast', 'OH': 'Midwest', 
    'OK': 'South', 'OR': 'West', 'PA': 'Northeast', 
    'RI': 'Northeast', 'SC': 'South', 'SD': 'Midwest', 
    'TN': 'South', 'TX': 'South', 'UT': 'West', 
    'VA': 'South', 'VT': 'Northeast', 'WA': 'West',
    'WI': 'Midwest', 'WV': 'South', 'WY': 'West'
}

CONTINENT_ABREV_TO_NAME = {
    'NA': 'North America',
    'EU': 'Europe',
    'OC': 'Oceania',
    'AS': 'Asia',
    'AF': 'Africa',
    'SA': 'South America',
}


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)