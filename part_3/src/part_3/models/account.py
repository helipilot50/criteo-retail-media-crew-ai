from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, field_serializer, field_validator
from enum import Enum

class AccountType(str, Enum):
    supply = "supply"
    demand = "demand"

class Account(BaseModel):
    id: str
    name: str
    type: AccountType 
    subtype: Optional[str] = Field(default=None)
    countries: List[str]
    currency: str
    parentAccountLabel: Optional[str] = Field(default=None)
    timeZone: str
    companyName: Optional[str] = Field(default=None)

    def to_json(self) -> str:
        return self.model_dump_json()
    
   
