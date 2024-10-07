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
