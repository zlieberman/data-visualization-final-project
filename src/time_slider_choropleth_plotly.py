import plotly
import plotly.express as px
import pandas as pd
from typing import Optional
from cmath import inf

from config.constants import RAW_DATA_FILE
from get_input import input_to_geodata, get_connections_data

SUPPORTED_MAP_TYPES = ['country names', 'USA-states', 'ISO-3', 'geojson-id']
SUPPORTED_PLOT_TYPES = ['scatter']
MAP_TYPE_TO_SCOPE = {
    'country names': 'world',
    'USA-states': 'usa'
}


def draw_plot(data_path: str, plotType: str, connections_path: Optional[str] = None, dataInterpretation: str = 'real values'):
    if plotType in SUPPORTED_MAP_TYPES:
        time_slider_choropleth_plotly(data_path, plotType, connections_path, dataInterpretation)
    elif plotType in SUPPORTED_PLOT_TYPES:
        dynamic_node_graph_plotly(data_path, connections_path, plotType, dataInterpretation)
    else:
        raise ValueError(f'type {plotType} is not in {SUPPORTED_MAP_TYPES} or {SUPPORTED_PLOT_TYPES}, please enter a supported type and try again')
        

def dynamic_node_graph_plotly(data_path: str, connections_path: str, plotType: str, dataInterpretation: str = 'real values'):
    inputDf = pd.read_csv(RAW_DATA_FILE)

    # read in connections data
    if connections_path is not None:
        # connectionsDf = get_connections_data(connections_path, inputDf['name'])
        pass

    xCol = 'cases'
    yCol = 'deaths'
    sizeCol = 'cases_avg'
    indexCol = 'state'

    maxX = inputDf[xCol].max()
    minX = inputDf[xCol].min()
    maxY = inputDf[yCol].max()
    minY = inputDf[yCol].min()

    fig = px.scatter(
        inputDf, x=xCol, y=yCol, animation_frame="date", animation_group=indexCol,
        size=sizeCol, color=indexCol, hover_name=indexCol,
        log_x=True, size_max=55, range_x=[minX,maxX], range_y=[minY,maxY]
    )

    fig["layout"].pop("updatemenus") # optional, drop animation buttons
    fig.show()


def time_slider_choropleth_plotly(data_path: str, mapType: str, connections_path: Optional[str] = None, dataInterpretation: str = 'real values'):
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

    # https://support.sisense.com/kb/en/article/plotly-choropleth-with-slider-map-charts-over-time
    data_slider = []
    for year in times:
        inputDf[f'{year}_text'] = connectionsDf[int(year)].values if connections_path else ''
        data_each_yr = dict(
            type='choropleth',
            locations = inputDf['name'],
            z=inputDf[year].astype(float),
            zmin=allTimeMin,
            zmax=allTimeMax,
            locationmode=mapType,
            colorscale = 'reds',
            colorbar= {'title':'Petroleum Exports Value in USD'},
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
                    label=f'Year {times[i]}')
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title ='Petroleum exports by country since 2000', geo=dict(scope=MAP_TYPE_TO_SCOPE[mapType]),
                sliders=sliders)

    fig = dict(data=data_slider, layout=layout)

    plotly.offline.iplot(fig)