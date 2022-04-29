from curses.ascii import US
import os
from site import addusersitepackages
import pandas as pd
from typing import Optional, Callable, List
import datetime
from config.constants import CONTINENT_ABREV_TO_NAME, DATASET1_PATH, DATASET2_PATH, MERGED_FILE_PATH, RAW_DATA_FILE_PATH, PROCESSED_DATA_FILE_PATH, US_STATE_TO_ABREV, USA_STATES_TO_REGION, WTO_TO_GEOPANDAS_COUNTRY_NAMES
import pycountry_convert as pc


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


def drop_entries_from_CSV(filename: str, dropCols: List[str], dropRows: List[str]):
    inputDf = pd.read_csv(filename, index_col=0)
    inputDf = inputDf.drop(dropCols, axis=1)
    inputDf = inputDf.drop(dropRows, axis=0)
    inputDf.to_csv(filename)


def getContinentFromCountry(countryName: str):
    try:
        country_code = pc.country_name_to_country_alpha2(countryName, cn_name_format="default")
    except:
        return "Invalid"
    continent_name = pc.country_alpha2_to_continent_code(country_code)
    return CONTINENT_ABREV_TO_NAME[continent_name]


def addContinentCol(file: str, numHeaderRows: int = 0):
    """
    Add a column with the continent abbreviation for each country in the csv file
    """
    csv = pd.read_csv(file, skiprows=numHeaderRows)
    def applyContinentFromCountry(row):
        return getContinentFromCountry(row.iloc[0])

    temp = csv.apply(lambda row: applyContinentFromCountry(row), axis=1)
    csv.insert(1,'Continent',temp)
    csv['Continent'] = csv['Continent'].astype(str)
    csv.set_index(csv.columns[0], inplace=True)
    outfile = file[0:file.index('.csv')] + '_new.csv'
    csv.to_csv(outfile)


def addUSStateRegionCol(filename: str):
    """
    Add a column with the region in the US that a state is 
    """
    inputDf = pd.read_csv(filename)

    regionCol = []
    for i, row in inputDf.iterrows():
        stateName = row['state']
        if stateName in US_STATE_TO_ABREV:
            regionCol.append(USA_STATES_TO_REGION[US_STATE_TO_ABREV[stateName]])
        else:
            regionCol.append('Invalid')

    inputDf['Region'] = regionCol
    inputDf.set_index(inputDf.columns[0], inplace=True)
    inputDf.to_csv(filename)


def merge_raw_datasets(rawfile1: str, rawfile2: str, mergeCols: List[str], outfile: str):
    df1 = pd.read_csv(rawfile1)
    df2 = pd.read_csv(rawfile2)

    mergedDf = df1.merge(df2, how='inner', on=mergeCols)
    mergedDf.set_index(df1.columns[0], inplace=True)
    mergedDf.to_csv(outfile)


def fill_data(filename: str):
    """
    Fill tbe first timestamp with empty data for any entities that don't have
    data for that timestamp. Necessary to dipslay properly with plotly.

    NOTE: this needs to be modified, it is hard coded specifically for covid.csv
    """
    inputDf = pd.read_csv(filename)
    timestamps = inputDf['Year'].unique().tolist()
    entities = inputDf['Country'].unique().tolist()
    earlestTime = timestamps[0]
    segmentedDf = inputDf[inputDf['Year'] == earlestTime]
    missingEntities = list(set(entities) - set(segmentedDf['Country'].unique().tolist()))
    for entity in missingEntities:
        if entity in US_STATE_TO_ABREV:
            abrev = US_STATE_TO_ABREV[entity]
        newRow = {
            'Country': entity,
            'Continent': getContinentFromCountry(entity),
            #'region': USA_STATES_TO_REGION[abrev],
            'Year': earlestTime,
            'GDP per capita': 0,
            'Mortality': 0,
        }
        inputDf = inputDf.append(newRow, ignore_index=True)
    inputDf.set_index(inputDf.columns[0], inplace=True)
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

    #base = datetime.datetime.strptime('1/21/20', '%m/%d/%y')
    #date_list = [datetime.datetime.strftime(base + datetime.timedelta(days=x), '%-m/%-d/%-y') for x in range(51)]
    #dropRows = ['AS', 'GU', 'MP', 'Virgin Islands', 'PR']
    #drop_entries_from_CSV(RAW_DATA_FILE_PATH, dropCols=[], dropRows=date_list)
    addContinentCol(MERGED_FILE_PATH)
    #merge_raw_datasets(DATASET1_PATH, DATASET2_PATH, ['Country', 'Year'], MERGED_FILE_PATH)
    #fill_data(RAW_DATA_FILE_PATH)
    #addUSStateRegionCol(RAW_DATA_FILE_PATH)