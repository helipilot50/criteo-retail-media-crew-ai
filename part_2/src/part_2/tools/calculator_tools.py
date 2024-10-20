from crewai_tools import BaseTool
from langchain.tools import tool


class CalculatorTool(BaseTool):
  """
  Make a calculation
  Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc.
  The input to this tool should be a mathematical expression, a couple examples are `200*7` or `5000/2*10`
  """

  name:str = "Make a calculation"
  description:str = "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical expression, a couple examples are `200*7` or `5000/2*10`"
  def _run(operation):
    return eval(operation)
  
  from crewai_tools import tool

class SumListTool(BaseTool):
  """
  Sum List Tool
  Useful for when you need to sum a list of numbers.
  """

  name:str = "Sum List Tool"
  description:str = "Useful for when you need to sum a list of numbers."
  def _run(numbers):
    return sum(numbers)

class CountListTool(BaseTool):
  """
  Count List Tool
  Useful for when you need to count the number of items in a list.
  """

  name:str = "Count List Tool"
  description:str = "Useful for when you need to count the number of items in a list."
  def _run(items):
    return len(items)