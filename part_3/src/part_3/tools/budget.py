from datetime import date
from langchain.tools import tool


@tool("venue budget calculator")
def venue_budget_calculator(budget: float, venues: dict) -> float:
    """
    Calculates the budget for each venue
    """
    total_capacity = sum(venues.values())

    for venue, capacity in venues.items():
        venues[venue]["budget"] = (capacity / total_capacity) * budget

    return venues

@tool("calculate monthly pacing")
def calculate_monthly_pacing(budget: float, startDate: date, endDate:date) -> float:
    """
    Calculates the monthly pacing for a campaign
    """
    num_months = (endDate.year - startDate.year) * 12 + endDate.month - startDate.month
    return budget / num_months