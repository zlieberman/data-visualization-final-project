import plotly
from get_input import input_to_geodata, get_connections_data

def time_slider_choropleth_plotly(data_path: str, connections_path: str):
    inputDf = input_to_geodata(data_path)

    times = ['2000', '2005', '2010', '2015']

    # read in connections data
    if connections_path is not None:
        connectionsDf = get_connections_data(connections_path, inputDf['name'])

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

        data_slider.append(data_each_yr)

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