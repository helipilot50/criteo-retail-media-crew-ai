from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
from crewai_tools import BaseTool, tool


plot_colors = [
    "blue",
    "red",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "brown",
    "grey",
    "black",
]

@tool("Bar Chart Creator")
def bar_chart_tool(
    categories: List,
    values: List[List[float]],
    x_label: str,
    y_label: str,
    labels: list[str],
    title: str,
    file_name: Optional[str] = None,
    path: Optional[str] = None,
):
    """
    Create a bar chart using MatPlotLib.
    Args:
        categories (List): The categories to plot.
        values (List[List[float]]): The values to plot.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        labels (list[str]): The labels for the plot.
        title (str): The title of the plot.
        file_name (Optional[str]): The name of the file to save the plot.
        path (Optional[str]): The path to save the plot.
    """
    print("Creating bar chart")
    print("categories", categories)
    print("values", values)
    print("x_label", x_label)
    print("y_label", y_label)
    print("labels", labels)
    print("title", title)
    print("file_name", file_name)
    print("path", path)

    plt.clf()

    # X-axis positions
    x = np.arange(len(categories))
    width = 0.35  # Width of the bars

    # Plotting
    fig, ax = plt.subplots()
    for i in range(len(values)):
        ax.bar(x, values[i], width, label=labels[i], color=plot_colors[i])

    # Adding labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.legend()
    # Save plot
    if file_name and path:
        plt.savefig(f"{path}/{file_name}")
    ax = None
    return f"Bar chart created for {title}"


@tool("Pie Chart Creator")
def pie_chart_tool(
    values: List,
    labels: List[str],
    title: str,
    file_name: str = None,
    path: Optional[str] = None,
):
    """
    Create a pie chart using MatPlotLib.
    Args:
        values (List): The values to plot.
        title (str): The title of the plot.
        file_name (str): The name of the file to save the plot.
    """
    full_file_name = ""
    if path:
        full_file_name = path + "/"
    full_file_name = full_file_name + file_name

    plt.clf()
    # Create pie plot
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    # Add title
    plt.title(title)
    plt.legend(labels, loc="best")
    # Save plot
    plt.savefig(full_file_name)
    return f"Pie chart created: {title}"
