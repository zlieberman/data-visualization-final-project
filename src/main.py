from config.constants import (
    COLORBAR_TITLE,
    DATA_INTERPRETATION,
    PLOT_TITLE,
    PROCESSED_DATA_FILE_PATH, 
    NODES_FILE_PATH,
    PLOT_TYPE,
    RAW_DATA_FILE_PATH,
)
from time_slider_choropleth_plotly import draw_plot


def main():
    data_path = PROCESSED_DATA_FILE_PATH
    if PLOT_TYPE == 'scatter':
        data_path = RAW_DATA_FILE_PATH

    draw_plot(
        data_path=data_path, 
        plotType=PLOT_TYPE,
        plotTitle=PLOT_TITLE,
        colorbarTitle=COLORBAR_TITLE,
        dataInterpretation=DATA_INTERPRETATION,
    )


if __name__ == '__main__':
    main()