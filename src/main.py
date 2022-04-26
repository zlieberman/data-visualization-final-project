import os
import pandas as pd
import numpy as np
import geopandas
import folium
from folium.plugins import TimeSliderChoropleth
from config.constants import (
    PROCESSED_DATA_FILE_PATH, 
    OUTPUT_HTML_PATH, 
    NODES_FILE_PATH,
)
import branca.colormap as cm
from shapely.geometry import LineString
import plotly
from typing import List


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


def main_plotly(data_path: str, connections_path: str):
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


def main():
    inputDf = input_to_geodata(PROCESSED_DATA_FILE_PATH)
    # create a folium map, min_zoom/max_bounds ensures the user can only see one copy of the map
    world_map = folium.Map(min_zoom=2, max_bounds=True)
    # choropleth maps use changes in color to represent data
    # TimeSliderChoropleth needs two parameters, the geo data and the style dict
    # https://notebook.community/ocefpaf/folium/examples/TimeSliderChoropleth
    times = inputDf.columns[7:]
    earliest_time = times[0]
    n_periods = len(times)

    datetime_index = pd.date_range(earliest_time, periods=n_periods, freq="Y")
    dt_index_epochs = datetime_index.astype(int) // 10 ** 9
    dt_index = dt_index_epochs.astype("U10")  

    inputDf.rename(columns={time: dt_index[i] for i, time in enumerate(times)}, inplace=True)

    # map of coordinates to represent the center of each country
    center_coordinates = {}
    for i, row in inputDf.iterrows():
        center_coordinates[row['Reporting_Economy']] = row['geometry'].centroid

    print(center_coordinates.keys())

    # draw polylines to represent connections between countries
    nodesDf = pd.read_csv(NODES_FILE_PATH)
    nodeGeometry = []
    for i, row in nodesDf.iterrows():
        print(row)
        row['Reporting_Economy'] = f'{row["Reporting_Economy"]}->{row["Partner_Economy"]}'
        for toNode in row:
            #print(toNode)
            trade_line = LineString([center_coordinates[row['Reporting_Economy'], center_coordinates[row['Partner_Economy']]]])
            nodeGeometry.append(trade_line)
            #trade_arc = folium.PolyLine(locations=[[0, 0], [-71, 40]], color='black')
            #world_map.add_child(trade_arc)

    nodesDf['geometry'] = nodeGeometry
    print(nodesDf)
            
    styledict = {}
    for location_idx, row in inputDf.iterrows():
        newLocationStyleEntry = {}
        for period in dt_index:
            newLocationStyleEntry[period] = {
                'color': row[period],
                'opacity': 0.7,
            }
        styledict[location_idx] = newLocationStyleEntry

    max_color, min_color, max_opacity, min_opacity = 0, 0, 0, 0

    for country, data in styledict.items():
        color_data = [timestamp_data['color'] for _, timestamp_data in data.items()]
        opacity_data = [timestamp_data['opacity'] for _, timestamp_data in data.items()]
        max_color = max(max_color, max(color_data))
        min_color = min(max_color, min(color_data))
        max_opacity = max(max_color, min(opacity_data))
        max_opacity = min(max_color, min(opacity_data))

    # convert values in the styledict to colors using a color map
    #cmap = linear.PuRd_09.scale(min_color, max_color)
    cmap = cm.LinearColormap(
        ['green', 'yellow', 'red'],
        vmin=min_color, vmax=max_color
    )

    for country, data in styledict.items():
        for timestamp, timestamp_data in data.items():
            timestamp_data['color'] = cmap(timestamp_data['color'])[:7]

    print(inputDf['geometry'][0])

    TimeSliderChoropleth(
        inputDf.to_json(),
        styledict=styledict,
    ).add_to(world_map)

    """
    Choropleth(
        geo_data=inputDf,
        name='choropleth',
        data=inputDf,
        columns=['Reporting Economy', '2015'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='GDP and trade partners',
    ).add_to(world_map)
    """

    # save the map in html format
    world_map.save(os.path.join(OUTPUT_HTML_PATH, 'test.html'))


if __name__ == '__main__':
    main_plotly(PROCESSED_DATA_FILE_PATH, NODES_FILE_PATH)
