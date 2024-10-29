from typing import Any
from crewai_tools import BaseTool
from crewai_tools import tool


@tool("Calculator Tool")
def calculator_tool(operation):
  """
  Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical expression, a couple examples are `200*7` or `5000/2*10`
  """
  return eval(operation)
  
 


@tool("Sum List Tool")
def sum_list_tool(numbers: list[float|int]):
  """
  Useful for when you need to sum a list of numbers. The input to this tool should be a list of numbers, a couple examples are `[1, 2, 3, 4, 5]` or `[10, 20, 30, 40, 50]`
  """
  return sum(numbers)



@tool("Count List Tool")
def count_list_tool(items: list[Any]):
  """
  Useful for when you need to count the number of items in a list. The input to this tool should be a list of items, a couple examples are `[1, 2, 3, 4, 5]` or `['apple', 'banana', 'cherry', 'date', 'elderberry']`
  """
  return len(items)