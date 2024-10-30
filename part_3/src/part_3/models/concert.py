from pydantic import BaseModel, field_serializer, field_validator
from typing import List, Optional
from datetime import date, datetime

from part_3.src.part_3.models.campaign import Campaign
from part_3.src.part_3.models.lineitem import LineitemList


class Concert(BaseModel):
    name: str
    date: date
    venue: str
    city: str
    country: str
    seatingCapacity: int
    digitalAdvertisingBudget: float

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value

    @field_serializer("date")
    def serialize_date(self, thedate: date) -> str:  # type: ignore
        return thedate.strftime("%Y-%m-%d")


class Tour(BaseModel):
    name: str
    year: str
    description: str
    concerts: Optional[List[Concert]]


class ConcertCampaign(BaseModel):
    campaign: Campaign
    lineitems: LineitemList
