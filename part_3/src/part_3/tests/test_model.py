from datetime import datetime, date
import json
from part_3.models.lineitem import (
    LineitemBidStrategy,
    LineitemStatus,
    NewAuctionLineitem,
)
from part_3.models.campaign import (
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
