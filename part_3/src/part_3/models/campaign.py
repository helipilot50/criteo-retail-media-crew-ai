import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class CampaignType(str, Enum):
    auction = "auction"
    preferred = "preferred"

class CampaignStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class ViewAttributionWindow(str, Enum):
    none = "none"
    sevenD = "7D"
    fourteenD = "14D"
    thirtyD = "30D"
    unknown = "unknown"

class ClickAttributionWindow(str, Enum):
    sevenD = "7D"
    fourteenD = "14D"
    thirtyD = "30D"
    unknown = "unknown"

class ClickAttributionScope(str, Enum):
    unknown = "unknown"
    sameSkuCategory = "sameSkuCategory"
    sameSku = "sameSku"
    sameSkuBrandCategory = "sameSkuBrandCategory"

class ViewAttributionScope(str, Enum):
    sameSkuCategory = "sameSkuCategory"
    sameSku = "sameSku"
    sameSkuBrandCategory = "sameSkuBrandCategory"

class NewCampaign(BaseModel):
    name: str
    startDate: datetime.date
    endDate: datetime.date
    budget: Optional[float]
    monthlyPacing: Optional[float]
    dailyBudget: Optional[float]
    isAutoDailyPacing:bool=False
    dailyPacing:Optional[float]
    type: Optional[CampaignType]
    clickAttributionWindow: ClickAttributionWindow
    viewAttributionWindow:ViewAttributionWindow
    clickAttributionScope:ClickAttributionScope
    viewAttributionScope:ViewAttributionScope
    
