from config.constants import (
    DATA_INTERPRETATION,
    PROCESSED_DATA_FILE_PATH, 
    NODES_FILE_PATH,
    PLOT_TYPE,
)
from time_slider_choropleth_plotly import draw_plot


def main():
    draw_plot(
        data_path=PROCESSED_DATA_FILE_PATH, 
        plotType=PLOT_TYPE,
        dataInterpretation=DATA_INTERPRETATION,
    )


if __name__ == '__main__':
    main()