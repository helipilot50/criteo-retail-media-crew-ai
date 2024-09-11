from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
from crewai_tools import BaseTool


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


class BarChartTool(BaseTool):
    """
    Used to create a bar chart using MatPlotLib.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Bar Chart Creator"
    description: str = (
        "Useful to create a bar chart using MatPlotLib. The input to this tool should be a list of categories and a list of values, the title and optionally a file name to save the plot."
    )

    def _run(
        self,
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


class PieChartTool(BaseTool):
    """
    Used to create a pie chart using MatPlotLib.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Create a pie chart"
    description: str = (
        "Useful to create a pie chart using MatPlotLib. The input to this tool should be a list of categories and a list of values, the title and optionally a file name to save the plot."
    )

    def _run(
        self,
        values: List,
        labels: List[str],
        title: str,
        file_name: Optional[str] = None,
    ):
        """
        Create a pie chart using MatPlotLib.
        Args:
            values (List): The values to plot.
            title (str): The title of the plot.
            file_name (Optional[str]): The name of the file to save the plot.
        """
        plt.clf()
        # Create pie plot
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        # Add title
        plt.title(title)
        plt.legend(labels, loc="best")
        # Save plot
        if file_name:
            plt.savefig(file_name)
        return f"Pie chart created: {title}"