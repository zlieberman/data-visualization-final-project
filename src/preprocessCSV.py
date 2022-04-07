import os
import pandas as pd
from config.constants import RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH



def preprocessCSV(infile: str, outfile: str):
    originalCSV = pd.read_csv(infile, skiprows=2)
    for i in range(originalCSV.shape[0]):
        if not (originalCSV.loc[i]["Product/Sector"] == "SI3_AGG - TO - Total merchandise"):
            originalCSV.drop(i, axis=0, inplace=True)
    originalCSV.set_index("Reporting Economy", inplace=True)
    print(originalCSV)
    originalCSV.to_csv(outfile)


if __name__ == '__main__':
    preprocessCSV(RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH)