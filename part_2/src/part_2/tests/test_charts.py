import os
from part_2.tests.utils import full_file_path
from part_2.tools.charts import BarChartTool, PieChartTool
import matplotlib.pyplot as plt
import numpy as np


def test_bar_chart_tool():
    file_name = full_file_path("test_bar_chart.png")
    if os.path.exists(file_name):
        os.remove(file_name)

    bar = BarChartTool()
    chart = bar._run(
        categories=[
            "2020-01-02",
            "2020-04-07",
            "2020-04-20",
            "2020-04-25",
            "2020-06-30",
            "2020-08-16",
            "2020-09-27",
            "2020-10-23",
            "2020-11-11",
            "2020-12-02",
            "2020-12-12",
            "2020-12-23",
            "2021-01-20",
            "2021-01-22",
            "2021-03-15",
            "2021-03-27",
            "2021-04-20",
            "2021-04-25",
            "2021-06-30",
            "2021-08-09",
            "2021-09-16",
            "2021-09-24",
            "2021-10-20",
            "2021-11-01",
            "2021-11-10",
            "2021-11-26",
            "2021-12-13",
            "2022-01-22",
            "2022-02-05",
            "2022-02-09",
            "2022-03-25",
            "2022-04-11",
            "2022-04-28",
            "2022-05-14",
            "2022-05-22",
            "2022-07-07",
            "2022-07-11",
            "2022-07-21",
            "2022-09-11",
            "2022-11-24",
            "2022-12-21",
            "2022-12-22",
            "2023-01-23",
            "2023-02-24",
            "2023-04-10",
            "2023-05-08",
            "2023-05-08",
            "2023-05-18",
            "2023-06-08",
            "2023-06-22",
            "2023-06-23",
            "2023-06-25",
            "2023-08-08",
            "2023-08-13",
            "2023-08-30",
            "2023-10-16",
            "2023-10-23",
            "2023-10-24",
            "2023-11-05",
        ],
        values=[
            [
                28.92,
                20.65,
                35.56,
                26.30,
                2.62,
                15.53,
                33.91,
                19.55,
                15.70,
                15.52,
                14.25,
                27.99,
                12.08,
                2.24,
                7.75,
                27.36,
                19.35,
                3.68,
                27.67,
                13.43,
                6.60,
                21.03,
                28.24,
                5.95,
                25.67,
                10.60,
                7.92,
                11.43,
                6.31,
                14.68,
                27.75,
                24.92,
                22.81,
                20.12,
                2.41,
                32.62,
                35.07,
                16.30,
                19.38,
                34.47,
                28.01,
                20.23,
                23.85,
                20.02,
                2.31,
                11.13,
                31.00,
                34.34,
                34.04,
                13.52,
                35.44,
                20.49,
                4.75,
                27.31,
                13.08,
                4.01,
                23.44,
                9.50,
                10.54,
            ],
            [
                10.50,
                4.79,
                4.46,
                5.85,
                10.13,
                5.75,
                0.98,
                12.17,
                0.38,
                11.72,
                0.74,
                5.01,
                6.92,
                0.13,
                3.66,
                4.41,
                0.61,
                0.77,
                11.03,
                2.66,
                7.92,
                6.66,
                6.44,
                10.54,
                9.44,
                3.95,
                1.37,
                12.81,
                10.33,
                1.44,
                5.58,
                1.84,
                12.21,
                5.80,
                2.51,
                9.00,
                2.64,
                6.82,
                9.33,
                7.63,
                9.19,
                5.94,
                9.76,
                2.62,
                11.80,
                8.96,
                11.65,
                7.19,
                2.67,
                7.85,
                1.70,
                11.27,
                9.62,
                8.45,
                9.04,
                13.63,
                1.60,
                9.60,
                11.41,
            ],
        ],
        x_label="Dates",
        y_label="Budgets",
        labels=["Auction", "Preferred"],
        title="Test Bar Chart",
        file_name=file_name,
    )
    assert os.path.exists(file_name)
    assert chart is not None


def test_pie_chart_tool():

    file_name = full_file_path("test_pie_chart.png")

    if os.path.exists(file_name):
        os.remove(file_name)

    pie = PieChartTool()
    chart = pie._run([1, 2, 3], "Test Pie Chart", file_name)
    assert os.path.exists(file_name)
    assert chart is not None
