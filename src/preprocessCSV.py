import os
import pandas as pd
from typing import Optional, Callable
from config.constants import RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH


def preprocessCSV(infile: str, outfile: str, numHeaderRows: int=0, indexCol: Optional[str]=None, customFilter: Optional[Callable[[pd.DataFrame], None]]=None):
    originalCSV = pd.read_csv(infile, skiprows=numHeaderRows)
    print(originalCSV)
    if customFilter is not None:
        customFilter(originalCSV)
    print(originalCSV)
    if indexCol is not None:
        originalCSV.set_index(indexCol, inplace=True)

    originalCSV.to_csv(outfile)


"""
Input data specific filters for preprocesCSV()
"""


def getWTODataFilter(criteria: dict):
    def customFilter(df: pd.DataFrame):
        for col, value in criteria.items():
            for i in range(df.shape[0]):
                if not (df.loc[i][col] == value):
                    df.drop(i, axis=0, inplace=True)
    
    return customFilter


if __name__ == '__main__':
    
    criteria = { "Product/Sector": "SI3_AGG - TO - Total merchandise" }
    
    preprocessCSV(
        RAW_DATA_FILE_PATH, 
        PROCESSED_DATA_FILE_PATH, 
        numHeaderRows=2,
        indexCol="Reporting Economy",
        customFilter=getWTODataFilter(criteria),
    )