import geopandas
from typing import List
import pandas as pd
import numpy as np


def input_to_geodata(input_file: str):
    # get the input data
    inputDf = pd.read_csv(input_file)

    # get geographic data from geopandas so we know where to draw each country
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    """
    for i in range(world.shape[0]):
        print(world.loc[i]['name'])
    return
    """

    # merge the two dataframes so we have the data we want as well as each country's shape
    inputDf = world.merge(inputDf, how='left', left_on=['name'], right_on=['Reporting_Economy'])
    inputDf = inputDf.dropna(subset=['Reporting_Economy'])
    inputDf = inputDf.drop(['Reporting_Economy'], axis=1)

    return inputDf


def get_connections_data(connections_file_path: str, countries: List[str]):
    inputDf = pd.read_csv(connections_file_path)
    connectionsDf = pd.DataFrame(index=countries)

    years = ['2000', '2005', '2010', '2015']
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

    print(connectionsDf)
    return connectionsDf