from config.constants import (
    PROCESSED_DATA_FILE_PATH, 
    NODES_FILE_PATH,
)
from time_slider_choropleth_plotly import time_slider_choropleth_plotly


def main():
    time_slider_choropleth_plotly(
        data_path=PROCESSED_DATA_FILE_PATH, 
        connections_path=NODES_FILE_PATH,
    )


if __name__ == '__main__':
    main()