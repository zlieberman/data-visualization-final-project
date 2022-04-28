from curses.ascii import US
import os
import pandas as pd
from typing import Optional, Callable, List
import datetime
from config.constants import RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH, US_STATE_TO_ABREV, WTO_TO_GEOPANDAS_COUNTRY_NAMES


def preprocessCSV(
    infile: str, 
    outfile: str, 
    dateCol: str,
    valueCol: str,
    numHeaderRows: int=0, 
    indexCol: Optional[str]=None, 
    customFilter: Optional[Callable[[pd.DataFrame], None]]=None
):
    originalCSV = pd.read_csv(infile, skiprows=numHeaderRows)

    if customFilter is not None:
        customFilter(originalCSV)
        
    if indexCol is not None:
        originalCSV.set_index(indexCol, inplace=True)

    years = originalCSV[dateCol].unique()

    firstColName = originalCSV.columns[0]
    outputCSV = pd.DataFrame(index=originalCSV[firstColName].unique(), columns=years)

    for i in range(originalCSV.shape[0]):
        countryName = originalCSV.loc[i][firstColName]
        year = originalCSV.loc[i][dateCol]
        value = originalCSV.loc[i][valueCol]
        if countryName in outputCSV.index:
            outputCSV.loc[countryName][year] = value

    # convert country names from WTO to Geopandas formatting
    for inputName, outputName in WTO_TO_GEOPANDAS_COUNTRY_NAMES.items():
        if inputName in outputCSV.index:
            outputCSV.rename(index={inputName: outputName}, inplace=True)

    # sort dates if every column is a date column
    try:
        sortedCols = outputCSV.columns.tolist()
        sortedCols.sort(key=lambda date: datetime.datetime.strptime(date, "%m/%d/%y"))
        outputCSV = outputCSV.reindex(sortedCols, axis=1)
    except:
        pass

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

    outputDf = pd.DataFrame(index=US_STATE_TO_ABREV.keys(), columns=inputDf.columns[1:])

    for i, row in inputDf.iterrows():
        if row[firstCol] in US_STATE_TO_ABREV:
            outputDf[row[firstCol]] = US_STATE_TO_ABREV[row[firstCol]]

        return row

    #outputDf = inputDf.apply(lambda row: convert_names(row), axis=1)

    outputDf.set_index(firstCol, inplace=True)
    outputDf.to_csv(outputFile)


def drop_cols_from_CSV(filename: str, dropCols: List[str]):
    inputDf = pd.read_csv(filename, index_col=0)
    print(inputDf.columns.tolist())
    inputDf = inputDf.drop(dropCols, axis=1)
    inputDf.to_csv(filename)


if __name__ == '__main__':
    #state_names_to_abbreviation(RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH)
 
    #criteria = { "Product/Sector": "SI3_AGG - TO - Total merchandise" }
    
    #preprocessCSV(
    #    RAW_DATA_FILE_PATH, 
    #    PROCESSED_DATA_FILE_PATH, 
    #    dateCol='date',
    #    valueCol='cases',
    #    numHeaderRows=0,
    #)

    base = datetime.datetime.strptime('1/21/20', '%m/%d/%y')
    date_list = [datetime.datetime.strftime(base + datetime.timedelta(days=x), '%-m/%-d/%-y') for x in range(52)]
    drop_cols_from_CSV(PROCESSED_DATA_FILE_PATH, date_list)