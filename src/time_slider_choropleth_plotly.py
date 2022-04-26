import plotly
from get_input import input_to_geodata, get_connections_data
import plotly.graph_objects as go


def time_slider_choropleth_plotly(data_path: str, connections_path: str):
    inputDf = input_to_geodata(data_path)

    times = ['2000', '2005', '2010', '2015']

    # read in connections data
    if connections_path is not None:
        connectionsDf = get_connections_data(connections_path, inputDf['name'])

    # map of coordinates to represent the center of each country
    centerCoordinates = {}
    for i, row in inputDf.iterrows():
        centerCoordinates[row.name] = row['geometry'].centroid

    # https://support.sisense.com/kb/en/article/plotly-choropleth-with-slider-map-charts-over-time
    data_slider = []
    print(inputDf)
    for year in times:
        if connections_path is not None:
            inputDf[f'{year}_text'] = connectionsDf[year].values
        data_each_yr = dict(
            type='choropleth',
            locations = inputDf['name'],
            z=inputDf[year].astype(float),
            locationmode='country names',
            colorscale = 'greens',
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
        #data_slider.append(trade_data_each_yr)

    steps = []
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label=f'Year {times[i]}')
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(title ='Petroleum exports by country since 2015', geo=dict(scope='world'),
                sliders=sliders)

    fig = dict(data=data_slider, layout=layout)

    plotly.offline.iplot(fig)