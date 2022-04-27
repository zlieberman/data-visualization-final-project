from numpy import disp
import plotly
import plotly.express as px
import pandas as pd

from config.constants import RAW_DATA_FILE
from get_input import input_to_geodata, get_connections_data

SUPPORTED_MAP_TYPES = ['country names']
SUPPORTED_PLOT_TYPES = ['scatter']


def draw_plot(data_path: str, connections_path: str, plotType: str, dataInterpretation: str = 'real values'):
    if plotType in SUPPORTED_MAP_TYPES:
        time_slider_choropleth_plotly(data_path, connections_path, plotType, dataInterpretation)
    elif plotType in SUPPORTED_PLOT_TYPES:
        dynamic_node_graph_plotly(data_path, connections_path, plotType, dataInterpretation)
    else:
        raise ValueError(f'type {plotType} is not in {SUPPORTED_MAP_TYPES} or {SUPPORTED_PLOT_TYPES}, please enter a supported type and try again')
        

def dynamic_node_graph_plotly(data_path: str, connections_path: str, plotType: str, dataInterpretation: str = 'real values'):
    inputDf = pd.read_csv(RAW_DATA_FILE)

    times = ['2000', '2005', '2010', '2015']

    # read in connections data
    if connections_path is not None:
        # connectionsDf = get_connections_data(connections_path, inputDf['name'])
        pass

    maxX = inputDf['Value'].max()
    minX = inputDf['Value'].min()
    maxY = inputDf['rankx'].max()
    minY = inputDf['rankx'].min()

    fig = px.scatter(
        inputDf, x="Value", y="rankx", animation_frame="Year", animation_group="Reporting_Economy",
        size="Value", color="Reporting_Economy", hover_name="Reporting_Economy",
        log_x=True, size_max=55, range_x=[minX,maxX], range_y=[minY,maxY]
    )

    fig["layout"].pop("updatemenus") # optional, drop animation buttons
    fig.show()


def time_slider_choropleth_plotly(data_path: str, connections_path: str, mapType: str, dataInterpretation: str = 'real values'):
    inputDf, times = input_to_geodata(data_path, dataInterpretation)

    # read in connections data
    if connections_path is not None:
        connectionsDf = get_connections_data(connections_path, inputDf['name'])

    # map of coordinates to represent the center of each country
    centerCoordinates = {}
    for i, row in inputDf.iterrows():
        centerCoordinates[row.name] = row['geometry'].centroid

    # https://support.sisense.com/kb/en/article/plotly-choropleth-with-slider-map-charts-over-time
    data_slider = []
    #print(inputDf)
    for year in times:
        if connections_path is not None:
            inputDf[f'{year}_text'] = connectionsDf[int(year)].values
        data_each_yr = dict(
            type='choropleth',
            locations = inputDf['name'],
            z=inputDf[year].astype(float),
            locationmode=mapType,
            colorscale = 'greys',
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

    layout = dict(title ='Petroleum exports by country since 2000', geo=dict(scope='world'),
                sliders=sliders)

    fig = dict(data=data_slider, layout=layout)

    plotly.offline.iplot(fig)