import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/petroleumWorld.csv"
PROCESSED_DATA_FILE = "data/petroleum_input.csv"
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)
OUTPUT_HTML_PATH = os.path.join(ROOT_PATH, 'output')
NODES_FILE_PATH = os.path.join(ROOT_PATH, 'data/top5Petrol.csv')

# user controlled to determine how the data is visualized
PLOT_TYPE = 'country names' # 'scatter'
DATA_INTERPRETATION = 'percent change' # 'real values'


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)