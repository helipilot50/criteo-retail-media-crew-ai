from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_serializer, field_validator
from enum import Enum


class LineitemStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    scheduled = "scheduled"
    ended = "ended"
    budgetHit = "budgetHit"
    noFunds = "noFunds"
    archived = "archived"


class LineitemType(str, Enum):
    auction = "auction"
    preferred = "preferred"


class LineitemBidStrategy(str, Enum):
    unknown = "unknown"
    clicks = "clicks"
    conversion = "conversion"
    revenue = "revenue"


# RetailMediaAuctionLineItem
class AuctionLineitem(BaseModel):
    """
    Line Item ID
    """

    id: str
    """
    Campaign ID
    """
    campaignId: str
    """
    Line item name; must be unique within a campaign
    """
    name: str
    """
    ID of the retailer the line item serves on
    """
    targetRetailerId: str
    """
    Line item start date in the account timeZone
    """
    startDate: date
    """
    Line item end date in the account timeZone; serves indefinitely if omitted or set to null
    """
    endDate: Optional[date] = None
    """
    Line item lifetime spend cap; uncapped if omitted or set to null
    """
    budget: Optional[float] = None
    """
    Amount the line item has already spent
    """
    budgetSpent: float
    """
    Amount the line item has remaining until cap is hit; null if budget is uncapped
    """
    budgetRemaining: float
    """
    Amount the line item can spend per calendar month in the account timeZone; 
    resets each calendar month; uncapped if omitted or set to null
    """
    monthlyPacing: Optional[float] = None
    """
    Amount the line item can spend per day 
    in the account timeZone; resets each day; 
    overwritten by a calculation if isAutoDailyPacing is configured; 
    uncapped if omitted or set to null
    """
    dailyPacing: Optional[float] = None
    """
    To activate, either line item endDate and budget, 
    or monthlyPace, must be specified; 
    overwrites dailyPacing with a calculation if not set prior
    """
    isAutoDailyPacing: bool
    """
    Bid algorithm optimizing for sales conversions, sales revenue, or clicks
    """
    bidStrategy: LineitemBidStrategy
    """
    If optimizing for conversion or revenue, 
    a target average amount to bid because each bid 
    is modulated up or down by our optimization algorithm; 
    bids stay constant if optimizing for clicks; must meet minBid 
    for line item to serve; minBid depends on selected products 
    and is retrieved through the catalog; input excludes platform fees
    """
    targetBid: Optional[float] = None
    """
    If optimizing for conversion or revenue, 
    the maximum amount allowed to bid for each bid; 
    respected regardless of targetBid; 
    must meet minBid for line item to serve; 
    minBid depends on selected products and is retrieved through the catalog; 
    bidding is uncapped if omitted or set to null; 
    does not apply if optimizing for clicks; 
    input excludes platform fees
    """
    maxBid: Optional[float] = None
    """
    Line item status; can only be updated by a user 
    to active or paused; all other values are applied 
    automatically depending on flight dates, financials, 
    or missing attributes required for line item to serve
    """
    status: LineitemStatus
    """
    Timestamp in UTC of line item creation
    """
    createdAt: datetime
    """
    Timestamp in UTC of last line item update
    """
    updatedAt: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("startDate", "endDate")
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value

    @field_serializer("startDate", "endDate")
    def serialize_date(self, thedate: date) -> str:
        return thedate.strftime("%Y-%m-%d")


class NewAuctionLineitem(BaseModel):
    name: str
    startDate: date
    targetRetailerId: str
    endDate: Optional[date] = None
    status: LineitemStatus = LineitemStatus.draft
    budget: Optional[float] = None
    targetBid: Optional[float] = None
    maxBid: Optional[float] = None
    monthlyPacing: Optional[float] = None
    dailyPacing: Optional[float] = None
    isAutoDailyPacing: bool = False
    bidStrategy: LineitemBidStrategy = LineitemBidStrategy.unknown

    @field_validator("startDate", "endDate")
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value

    @field_serializer("startDate", "endDate")
    def serialize_date(self, thedate: date) -> str:
        return thedate.strftime("%Y-%m-%d")
