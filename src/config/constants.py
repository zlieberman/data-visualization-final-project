import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/petroleumWorld.csv"
PROCESSED_DATA_FILE = "data/petroleum_input.csv"
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)
OUTPUT_HTML_PATH = os.path.join(ROOT_PATH, 'output')
NODES_FILE_PATH = os.path.join(ROOT_PATH, 'data/top5Petrol.csv')

# plot types
PLOT_TYPE = 'scatter' # 'country names'


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)