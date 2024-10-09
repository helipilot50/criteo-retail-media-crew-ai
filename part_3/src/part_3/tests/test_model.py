from datetime import datetime, date
import json
from part_3.models.lineitem import (
    LineitemBidStrategy,
    LineitemStatus,
    NewAuctionLineitem,
)
from part_3.models.campaign import (
    Campaign,
    CampaignType,
    ClickAttributionScope,
    ClickAttributionWindow,
    NewCampaign,
    ViewAttributionScope,
    ViewAttributionWindow,
)
from crewai_tools import (
    FileWriterTool,
)


class TestClass:
    name: str = "A tool"
    description: str = "does stuff with lineitem"

    def _run(self, lineitem: NewAuctionLineitem):
        return do_something_with_lineitem(lineitem)


def do_something_with_lineitem(lineitem: NewAuctionLineitem) -> NewAuctionLineitem:
    aDict = lineitem.model_dump()
    assert aDict is not None
    return lineitem


def test_new_auction_lineitem():
    new_lineitem = NewAuctionLineitem(
        name="test",
        startDate=date(2022, 1, 1),
        status=LineitemStatus.draft,
        targetRetailerId="test",
        bidStrategy=LineitemBidStrategy.clicks,
        isAutoDailyPacing=False,
    )
    assert new_lineitem is not None

    result = do_something_with_lineitem(new_lineitem)
    assert result is not None


def test_new_campaign():
    fileWriter = FileWriterTool()
    campaign = NewCampaign(
        name="Jimmy Carr Concert Tour 2030 ",
        startDate="2030-01-01",
        endDate=date(2030, 12, 31),
        budget=1280000,
        isAutoDailyPacing=False,
        type=CampaignType.auction,
        clickAttributionWindow=ClickAttributionWindow.thirtyDays,
        viewAttributionWindow=ViewAttributionWindow.none,
        clickAttributionScope=ClickAttributionScope.sameSkuCategory,
        viewAttributionScope=ViewAttributionScope.sameSkuCategory,
    )
    assert campaign is not None
    fileWriter._run(
        directory="output",
        filename=f"test_model_new_campaign.json",
        content=json.dumps(campaign.model_dump(), indent=2),
        overwrite=True,
    )


def test_campaign():
    fileWriter = FileWriterTool()
    campaign = Campaign(
        accountId="4",
        promotedBrandIds=[],
        budgetSpent=0.0,
        budgetRemaining=None,
        status="inactive",
        createdAt="2024-04-17T22:06:01+00:00",
        updatedAt="2024-04-17T22:06:01+00:00",
        type="auction",
        drawableBalanceIds=[],
        clickAttributionWindow="30D",
        viewAttributionWindow="1D",
        name="TEST CATIRE",
        budget=None,
        monthlyPacing=None,
        dailyPacing=None,
        isAutoDailyPacing=False,
        startDate="2024-04-17T04:00:00+00:00",
        # endDate="2024-04-18T03:59:59+00:00",
        endDate=None,
        clickAttributionScope=ClickAttributionScope.sameSku,
        viewAttributionScope=ViewAttributionScope.sameSku,
        companyName=None,
        onBehalfCompanyName=None,
        id="568557877387161600",
    )
    assert campaign is not None
    fileWriter._run(
        directory="output",
        filename=f"test_model_campaign.json",
        content=json.dumps(campaign.model_dump(), indent=2),
        overwrite=True,
    )
