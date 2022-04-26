import os
import pandas as pd
from typing import Optional, Callable
from config.constants import RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH


def preprocessCSV(infile: str, outfile: str, numHeaderRows: int=0, indexCol: Optional[str]=None, customFilter: Optional[Callable[[pd.DataFrame], None]]=None):
    originalCSV = pd.read_csv(infile, skiprows=numHeaderRows)

    if customFilter is not None:
        customFilter(originalCSV)
        
    if indexCol is not None:
        originalCSV.set_index(indexCol, inplace=True)

    years = originalCSV['Year'].unique()

    outputCSV = pd.DataFrame(index=originalCSV['Reporting_Economy'].unique(), columns=years)

    for i in range(originalCSV.shape[0]):
        countryName = originalCSV.loc[i]['Reporting_Economy']
        year = originalCSV.loc[i]['Year']
        value = originalCSV.loc[i]['Value']
        if countryName in outputCSV.index:
            outputCSV.loc[countryName][year] = value

    outputCSV.name = "Reporting_Economy"
    outputCSV.to_csv(outfile)


"""
Input data specific filters for preprocesCSV()
"""

# https://stats.wto.org/
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
        numHeaderRows=0,
    )