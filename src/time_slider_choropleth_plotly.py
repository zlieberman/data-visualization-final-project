import plotly
import plotly.express as px
import pandas as pd
from typing import Optional
from cmath import inf
import numpy as np

from config.constants import RAW_DATA_FILE
from get_input import input_to_geodata, get_connections_data

SUPPORTED_MAP_TYPES = ['country names', 'USA-states', 'ISO-3', 'geojson-id']
SUPPORTED_PLOT_TYPES = ['scatter']
MAP_TYPE_TO_SCOPE = {
    'country names': 'world',
    'USA-states': 'usa'
}


def draw_plot(
    data_path: str, 
    plotType: str, 
    plotTitle: str,
    colorbarTitle: Optional[str] = '',
    connections_path: Optional[str] = None, 
    dataInterpretation: str = 'real values'
):
    if plotType in SUPPORTED_MAP_TYPES:
        time_slider_choropleth_plotly(
            data_path, 
            plotType, 
            plotTitle, 
            colorbarTitle, 
            connections_path, 
            dataInterpretation
        )
    elif plotType in SUPPORTED_PLOT_TYPES:
        dynamic_node_graph_plotly(
            data_path, 
            plotTitle,
            connections_path,
            plotType, 
            dataInterpretation
        )
    else:
        raise ValueError(f'type {plotType} is not in {SUPPORTED_MAP_TYPES} or {SUPPORTED_PLOT_TYPES}, please enter a supported type and try again')
        

def dynamic_node_graph_plotly(
    data_path: str, 
    plotTitle: str,
    connections_path: str, 
    plotType: str, 
    dataInterpretation: str = 'real values'
):
    inputDf = pd.read_csv(data_path)


    # read in connections data
    if connections_path is not None:
        # connectionsDf = get_connections_data(connections_path, inputDf['name'])
        pass

    # For GDP data
    xCol = 'GDP per capita'
    yCol = 'Mortality'
    sizeCol = 'GDP per capita'
    indexCol = 'Country'
    dateCol = 'Year'
    colorCol = 'Continent'

    """
    # For Covid Data
    xCol = 'cases_avg_per_100k'
    yCol = 'deaths_avg_per_100k'
    sizeCol = 'cases_avg'
    indexCol = 'state'
    dateCol = 'date'
    colorCol = 'Region'
    """

    xCol = 'GDP per capita'
    yCol = 'Mortality'
    sizeCol = 'GDP'
    indexCol = 'Country'
    dateCol = 'Year'
    colorCol = 'Continent'

    # filter out invalid colorCol rows
    inputDf.drop(inputDf[(inputDf[colorCol] == 'Invalid') | (inputDf[colorCol] == None)].index, inplace=True)
    inputDf.dropna(inplace=True)

    print(inputDf)
    inputDf = inputDf.dropna()
    maxX = inputDf[xCol].max()
    minX = inputDf[xCol].min()
    maxY = inputDf[yCol].max()
    minY = inputDf[yCol].min()

    fig = px.scatter(
        inputDf, x=xCol, y=yCol, animation_frame=dateCol, animation_group=indexCol,
        size=sizeCol, color=colorCol, hover_name=indexCol,
        log_x=False, size_max=100, range_x=[minX-50,maxX+50], range_y=[minY-50,maxY+50]
    )

    fig.show()


def time_slider_choropleth_plotly(
    data_path: str, 
    mapType: str, 
    plotTitle: str,
    colorbarTitle: str,
    connections_path: Optional[str] = None, 
    dataInterpretation: str = 'real values'
):
    inputDf, times = input_to_geodata(data_path, dataInterpretation, mapType)

    # read in connections data
    if connections_path is not None:
        connectionsDf = get_connections_data(connections_path, inputDf['name'])

    # map of coordinates to represent the center of each country
    """
    centerCoordinates = {}
    for i, row in inputDf.iterrows():
        centerCoordinates[row.name] = row['geometry'].centroid
    """

    # get historical lows and highs so colorbar scale can be constant
    allTimeMax = -inf
    allTimeMin = inf
    for i, row in inputDf.iterrows():
        for time in times:
            allTimeMin = min(allTimeMin, row[time])
            allTimeMax = max(allTimeMax, row[time])

    allTimeMax = np.log10(allTimeMax)
    allTimeMin = np.log10(allTimeMin) if allTimeMin > 0 else 0

    # https://support.sisense.com/kb/en/article/plotly-choropleth-with-slider-map-charts-over-time
    data_slider = []
    for year in times:
        inputDf[year].fillna(0, inplace=True)
        inputDf[f'{year}_text'] = connectionsDf[int(year)].values if connections_path else inputDf[year]
        data_each_yr = dict(
            type='choropleth',
            locations = inputDf['name'],
            z=np.log10(inputDf[year]).astype(float),
            zmin=allTimeMin,
            zmax=allTimeMax,
            locationmode=mapType,
            colorscale = 'reds',
            colorbar= {'title': colorbarTitle},
            text=inputDf[f'{year}_text'],
        )

        """
        for i in range(connectionsDf.shape[0]):
            country = connectionsDf.iloc[i].name
            countryPartners = connectionsDf.iloc[i][year]
            for countryPartner in countryPartners:
                if country in centerCoordinates.index:
                    trade_data_each_yr = dict(
                        x=[centerCoordinates[country][0], centerCoordinates[countryPartner][0]],
                        y=[centerCoordinates[country][1], centerCoordinates[countryPartner][1]],
                        type='scatter',
                    )
        """

        data_slider.append(data_each_yr)

    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label=f'{times[i]}')
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title =plotTitle, geo=dict(scope=MAP_TYPE_TO_SCOPE[mapType]),
                sliders=sliders)

    fig = dict(data=data_slider, layout=layout)

    plotly.offline.iplot(fig)