import os
import pandas as pd
import geopandas
import folium
from folium.plugins import TimeSliderChoropleth
from config.constants import PROCESSED_DATA_FILE_PATH, OUTPUT_HTML_PATH
import json
import branca.colormap as cm
from branca.colormap import linear


def main():
    # get the input data
    inputDf = pd.read_csv(PROCESSED_DATA_FILE_PATH)
    # get geographic data from geopandas so we know where to draw each country
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # merge the two dataframes so we have the data we want as well as each country's shape
    inputDf = world.merge(inputDf, how='left', left_on=['name'], right_on=['Reporting Economy'])
    inputDf = inputDf.dropna(subset=['Reporting Economy'])
    inputDf = inputDf.drop(['Reporting Economy', 'Product/Sector'], axis=1)
    print(inputDf.columns)
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

    print(inputDf)

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
    main()
