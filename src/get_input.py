from curses.ascii import isdigit
import geopandas
from typing import List
import pandas as pd
import numpy as np

SUPPORTED_DATA_INTERPRETATIONS = ['real values', 'percent change']


def input_to_geodata(input_file: str, dataInterpretation: str = 'real values'):
    # get the input data
    inputDf = pd.read_csv(input_file)

    # get geographic data from geopandas so we know where to draw each country
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    """
    for i in range(world.shape[0]):
        print(world.loc[i]['name'])
    return
    """

    # get the first timestamp, for plots we assume the dataframe has a single value that 
    # varies each timestamp and has columns order chronologically labled with their timestamp
    timestamps = [col for col in inputDf.columns if col.isdigit()]

    # merge the two dataframes so we have the data we want as well as each country's shape
    inputDf = world.merge(inputDf, how='left', left_on=['name'], right_on=['name'])
    inputDf = inputDf.dropna(subset=['geometry', timestamps[0]])

    if dataInterpretation == 'percent change':
        # calculate percent change from previous timestamp for each row
        def percentChangeApplier(row: pd.Series):
            new_vals = []
            for j, timestamp in enumerate(timestamps[1:]):
                change = (row[timestamp] - row[timestamps[j-1]]) / row[timestamps[j-1]]
                if change > 0:
                    new_vals.append((change - 1) * 100)
                elif change < 0:
                    new_vals.append((1 - change) * 100)
                else:
                    new_vals.append(change)

            for i, val in enumerate(new_vals):
                row[timestamps[i+1]] = new_vals[i]

            return row

        inputDf = inputDf.apply(lambda row: percentChangeApplier(row), axis=1)          
        # drop the first timestamp since there is no percent change there
        inputDf = inputDf.drop([timestamps[0]], axis=1)
        timestamps.pop(0)
    elif dataInterpretation != 'real values':
        raise ValueError(f'Unsupported data interpretation method {dataInterpretation}, use one of {SUPPORTED_DATA_INTERPRETATIONS}')

    print(inputDf.head())  
    return inputDf, timestamps


def get_connections_data(connections_file_path: str, countries: List[str]):
    inputDf = pd.read_csv(connections_file_path)
    connectionsDf = pd.DataFrame(index=countries)

    years = inputDf['Year'].unique()
    num_countries = len(countries)
    # format each row of the dataframe to have a country name 
    # and a list of top trade partners by year from list formatted:
    # country, trade_partner, year, amount, rank
    for year in years:
        yearDf = inputDf.loc[inputDf['Year'] == int(year)]
        connectionsDf[year] = np.empty((num_countries, 0)).tolist()

        for i in range(yearDf.shape[0]):
            rowData = yearDf.iloc[i]
            countryName = rowData['Reporting_Economy']
            if countryName in connectionsDf.index:
                connectionsDf.loc[rowData['Reporting_Economy']][year].append(rowData['Partner_Economy'])

    print(connectionsDf.head())
    return connectionsDf