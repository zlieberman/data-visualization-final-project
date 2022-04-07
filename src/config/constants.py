import os


ROOT_PATH = os.path.abspath('.')
RAW_DATA_FILE = "data/WtoData_20220406190501.csv"
PROCESSED_DATA_FILE = "data/visualization_input.csv"
RAW_DATA_FILE_PATH = os.path.join(ROOT_PATH, RAW_DATA_FILE)
PROCESSED_DATA_FILE_PATH = os.path.join(ROOT_PATH, PROCESSED_DATA_FILE)


if __name__ == '__main__':
    print(RAW_DATA_FILE)
    print(ROOT_PATH)
    print(RAW_DATA_FILE_PATH)