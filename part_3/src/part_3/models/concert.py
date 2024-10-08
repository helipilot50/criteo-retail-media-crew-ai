from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date


class Concert(BaseModel):
    name: str
    date: date
    venue: str
    city: str
    country: str
    seatingCapacity: int
    digitalAdvertisingBudget: float

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Tour(BaseModel):
    name: str
    year: str
    description: str
    concerts: Optional[List[Concert]]

    model_config = ConfigDict(arbitrary_types_allowed=True)
