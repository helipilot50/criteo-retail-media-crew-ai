import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class LineitemStatus(str, Enum):
    active = "active"
    paused = "paused"
    scheduled = "scheduled"
    ended = "ended"
    budgetHit = "budgetHit"
    noFunds = "noFunds"
    draft = "draft"
    archived = "archived"


class LineitemType(str, Enum):
    auction = "auction"
    preferred = "preferred"


class LineitemBidStrategy(str, Enum):
    unknown = "unknown"
    clicks = "clicks"
    conversion = "conversion"
    revenue = "revenue"


class AuctionLineitem(BaseModel):
    id: str
    name: str
    campaignId: str
    status: LineitemStatus
    startDate: datetime.date
    endDate: Optional[datetime.date]
    budget: Optional[float]
    maxBid: Optional[float]
    bidStrategy: LineitemBidStrategy
    monthlyPacing: Optional[float]
    dailyPacing: Optional[float]
    targetBid: Optional[float]
    isAutoDailyPacing: bool
    targetRetailerId: str
    budgetSpent: float
    budgetRemaining: float
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class NewAuctionLineitem(BaseModel):
    name: str
    startDate: datetime.date
    status: LineitemStatus
    targetRetailerId: str
    bidStrategy: LineitemBidStrategy
    isAutoDailyPacing: bool
    endDate: Optional[datetime.date]
    budget: Optional[float]
    targetBid: Optional[float]
    maxBid: Optional[float]
    monthlyPacing: Optional[float]
    dailyPacing: Optional[float]

    model_config = ConfigDict(arbitrary_types_allowed=True)
