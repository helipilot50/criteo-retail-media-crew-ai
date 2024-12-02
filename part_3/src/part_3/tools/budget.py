from datetime import date
from langchain.tools import tool
from typing import List

from part_3.models.concert import Concert


@tool("venue budget calculator")
def concert_budget_calculator(budget: float, concerts: List[Concert]) -> List[Concert]:
    """
    Calculates the budget for each venue
    """
    total_capacity = sum(concerts.values())

    for concert, capacity in concerts.items():
        concerts[concert].budget = (capacity / total_capacity) * budget

    return concerts


@tool("calculate monthly pacing")
def calculate_monthly_pacing(budget: float, startDate: date, endDate: date) -> float:
    """
    Calculates the monthly pacing for a campaign
    """
    num_months = (endDate.year - startDate.year) * 12 + endDate.month - startDate.month
    return budget / num_months
