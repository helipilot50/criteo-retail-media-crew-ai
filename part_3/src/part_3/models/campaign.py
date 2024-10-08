from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_serializer, field_validator
from enum import Enum


class CampaignType(str, Enum):
    auction = "auction"
    preferred = "preferred"


class CampaignStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ViewAttributionWindow(str, Enum):
    oneDay = "1D"
    sevenDays = "7D"
    fourteenDays = "14D"
    thirtyDays = "30D"
    unknown = "unknown"
    none = "none"


class ClickAttributionWindow(str, Enum):
    sevenDays = "7D"
    fourteenDays = "14D"
    thirtyDays = "30D"
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
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    budget: Optional[float] = None
    monthlyPacing: Optional[float] = None
    isAutoDailyPacing: bool = False
    dailyPacing: Optional[float] = None
    type: Optional[CampaignType] = CampaignType.auction
    clickAttributionWindow: ClickAttributionWindow
    viewAttributionWindow: ViewAttributionWindow
    clickAttributionScope: ClickAttributionScope
    viewAttributionScope: ViewAttributionScope
    companyNames: Optional[str] = None
    drawableBalanceIds: Optional[List[str]] = None

    @field_validator("startDate", "endDate")
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value
    
    @field_serializer('startDate', 'endDate')
    def serialize_date(self, thedate: date) -> str:
        return thedate.strftime("%Y-%m-%d")
    
    class Config:
        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d"),
            CampaignType: lambda v: v.value,
            ClickAttributionWindow: lambda v: v.value,
            ViewAttributionWindow: lambda v: v.value,
            ClickAttributionScope: lambda v: v.value,
            ViewAttributionScope: lambda v: v.value,
        }


class UpdateCampaign(BaseModel):
    id: str
    name: Optional[str] = None
    isAutoDailyPacing: Optional[bool] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    type: Optional[CampaignType] = None
    drawableBalanceIds: Optional[List[str]] = None
    clickAttributionWindow: Optional[ClickAttributionWindow] = None
    viewAttributionWindow: Optional[ViewAttributionWindow] = None
    budget: Optional[float] = None
    monthlyPacing: Optional[float] = None
    dailyPacing: Optional[float] = None
    clickAttributionScope: Optional[ClickAttributionScope] = None
    viewAttributionScope: Optional[ViewAttributionScope] = None
    companyName: Optional[str] = None

    # model_config = ConfigDict(arbitrary_types_allowed=True)
    class Config:
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}


class Campaign(BaseModel):
    id: str
    accountId: str
    promotedBrandIds: List[str]
    budgetSpent: float
    budgetRemaining: Optional[float] = None
    status: CampaignStatus
    createdAt: datetime
    updatedAt: datetime
    type: CampaignType
    drawableBalanceIds: List[str]
    clickAttributionWindow: ClickAttributionWindow
    viewAttributionWindow: ViewAttributionWindow
    name: str
    budget: Optional[float] = None
    monthlyPacing: Optional[float] = None
    dailyPacing: Optional[float] = None
    isAutoDailyPacing: bool
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    clickAttributionScope: ClickAttributionScope
    viewAttributionScope: ViewAttributionScope
    companyName: Optional[str] = None

    # model_config = ConfigDict(arbitrary_types_allowed=True)
    class Config:
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}
