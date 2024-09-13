from crewai_tools import BaseTool


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