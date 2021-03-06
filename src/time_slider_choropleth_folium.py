import folium
from folium.plugins import TimeSliderChoropleth
import os
import pandas as pd
import branca.colormap as cm
from shapely.geometry import LineString
from src.config.constants import NODES_FILE_PATH, PROCESSED_DATA_FILE_PATH, OUTPUT_HTML_PATH 
from get_input import get_connections_data, input_to_geodata


def time_slider_choropleth_folium():
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
    nodesDf = get_connections_data(NODES_FILE_PATH)
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

    # save the map in html format
    world_map.save(os.path.join(OUTPUT_HTML_PATH, 'test.html'))