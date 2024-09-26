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
    startDate: Optional[datetime.date]
    endDate: Optional[datetime.date]
    budget: Optional[float]
    monthlyPacing: Optional[float]
    isAutoDailyPacing:bool=False
    dailyPacing:Optional[float]
    type: Optional[CampaignType]
    clickAttributionWindow: ClickAttributionWindow
    viewAttributionWindow:ViewAttributionWindow
    clickAttributionScope:ClickAttributionScope
    viewAttributionScope:ViewAttributionScope
    companyNames: Optional[str]
    drawableBalanceIds: Optional[List[str]]

class UpdateCampaign(BaseModel):
    id:str
    name:Optional[str]
    isAutoDailyPacing:Optional[bool]
    startDate:Optional[datetime.date]
    endDate:Optional[datetime.date]
    type:Optional[CampaignType]
    drawableBalanceIds:Optional[List[str]]
    clickAttributionWindow:Optional[ClickAttributionWindow]
    viewAttributionWindow:Optional[ViewAttributionWindow]
    budget:Optional[float]
    monthlyPacing:Optional[float]
    dailyPacing:Optional[float]
    clickAttributionScope: Optional[ClickAttributionScope]
    viewAttributionScope: Optional[ViewAttributionScope]
    companyName:Optional[str]
    
class Campaign(BaseModel):
    id: str
    accountId: str
    promotedBrandIds:List[str]
    budgetSpent:float
    budgetRemaining:Optional[float]
    status: CampaignStatus
    createdAt: datetime
    updatedAt: datetime
    type: CampaignType
    drawableBalanceIds:List[str]
    clickAttributionWindow: ClickAttributionWindow
    viewAttributionWindow: ViewAttributionWindow
    name: str
    budget:Optional[float]
    monthlyPacing:Optional[float]
    dailyPacing:Optional[float]
    isAutoDailyPacing:bool
    startDate:Optional[datetime.date]
    endDate:Optional[datetime.date]
    clickAttributionScope: ClickAttributionScope
    viewAttributionScope: ViewAttributionScope
    companyName:Optional[str]