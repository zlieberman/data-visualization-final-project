import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/manufacturingmWorld.csv"
PROCESSED_DATA_FILE = "data/manufacturing_input.csv"
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)
OUTPUT_HTML_PATH = os.path.join(ROOT_PATH, 'output')
NODES_FILE_PATH = os.path.join(ROOT_PATH, 'data/top5Manufacturing.csv')

# user controlled to determine how the data is visualized
PLOT_TYPE = 'country names' # 'scatter'
DATA_INTERPRETATION = 'percent change' # 'real values'

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


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)