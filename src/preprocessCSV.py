import os
import pandas as pd
from typing import Optional, Callable
from config.constants import RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH, US_STATE_TO_ABREV, WTO_TO_GEOPANDAS_COUNTRY_NAMES


def preprocessCSV(infile: str, outfile: str, numHeaderRows: int=0, indexCol: Optional[str]=None, customFilter: Optional[Callable[[pd.DataFrame], None]]=None):
    originalCSV = pd.read_csv(infile, skiprows=numHeaderRows)

    if customFilter is not None:
        customFilter(originalCSV)
        
    if indexCol is not None:
        originalCSV.set_index(indexCol, inplace=True)

    years = originalCSV['Year'].unique()

    firstColName = originalCSV.columns[0]
    outputCSV = pd.DataFrame(index=originalCSV[firstColName].unique(), columns=years)

    for i in range(originalCSV.shape[0]):
        countryName = originalCSV.loc[i][firstColName]
        year = originalCSV.loc[i]['Year']
        value = originalCSV.loc[i]['Value']
        if countryName in outputCSV.index:
            outputCSV.loc[countryName][year] = value

    for inputName, outputName in WTO_TO_GEOPANDAS_COUNTRY_NAMES.items():
        if inputName in outputCSV.index:
            #outputCSV[inputName].name = outputName
            outputCSV.rename(index={inputName: outputName}, inplace=True)

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


def petroleumDataFilter():
    pass


# specific functions to clean data

# this one will convert all state names to their abbreviations:
def state_names_to_abbreviation(inputFile: str, outputFile: str):
    inputDf = pd.read_csv(inputFile)

    firstCol = inputDf.columns[0]

    def convert_names(row: pd.Series):
        row[firstCol] = US_STATE_TO_ABREV[row[firstCol]]
        return row

    outputDf = inputDf.apply(lambda row: convert_names(row), axis=1)

    outputDf.set_index(firstCol, inplace=True)
    outputDf.to_csv(outputFile)


if __name__ == '__main__':
    state_names_to_abbreviation(RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH)

    """ 
    criteria = { "Product/Sector": "SI3_AGG - TO - Total merchandise" }
    
    preprocessCSV(
        RAW_DATA_FILE_PATH, 
        PROCESSED_DATA_FILE_PATH, 
        numHeaderRows=0,
    )
    """