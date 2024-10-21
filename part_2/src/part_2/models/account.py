from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, field_serializer, field_validator
from enum import Enum

class AccountType(str, Enum):
    supply = "supply"
    demand = "demand"

class Account(BaseModel):
    id: str
    name: str
    type: AccountType 
    subtype: Optional[str] = None
    countries: List[str]
    currency: str
    parentAccountLabel: Optional[str] = None
    timeZone: str
    companyName: Optional[str] = None
    
   
