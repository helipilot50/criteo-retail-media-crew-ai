import os
from chapter_2.tools.charts import BarChartTool, PieChartTool
import matplotlib.pyplot as plt
import numpy as np



def test_bar_chart_tool():
    file_name = 'output/test_bar_chart.png' 
    if os.path.exists(file_name):
        os.remove(file_name)
    bar = BarChartTool()
    chart = bar._run(categories=['A', 'B', 'C','D'], 
                    values=[[5, 7, 3, 4],
                    [1, 2, 1, 2]], 
                    x_label='X-axis',
                    y_label='Y-axis',
                    labels=["cats", "dogs"],
                    title='Test Bar Chart', 
                    file_name=file_name)
    assert os.path.exists(file_name)
    chart.show()

def test_pie_chart_tool():
    file_name = 'output/test_pie_chart.png'
    if os.path.exists(file_name):
        os.remove(file_name)
    bar = PieChartTool()
    chart = bar._run(['A', 'B', 'C'], [1, 2, 3], 'Test Pie Chart', file_name)
    assert os.path.exists(file_name)
    chart.show()

