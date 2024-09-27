import datetime
import json
from part_3.models.lineitem import (
    LineitemBidStrategy,
    LineitemStatus,
    NewAuctionLineitem,
)
from crewai_tools import BaseTool


class TestClass():
    name: str = "A tool"
    description: str = "does stuff with lineitem"

    def _run(self, lineitem: NewAuctionLineitem):
        return do_something_with_lineitem(lineitem)


def do_something_with_lineitem(lineitem: NewAuctionLineitem) -> NewAuctionLineitem:
    aDict = lineitem.model_dump()
    assert aDict is not None
    # print("aDict --> ", aDict)
    aJSON = lineitem.model_dump_json()
    assert aJSON is not None
    # print("aJSON --> ", aJSON)
    serialisedDict = json.dumps(aDict)
    assert serialisedDict is not None
    return lineitem


def test_new_auction_lineitem():
    test_new_auction_lineitem = NewAuctionLineitem(
        name="test",
        startDate=datetime.date(2022, 1, 1),
        status=LineitemStatus.draft,
        targetRetailerId="test",
        bidStrategy=LineitemBidStrategy.clicks,
        isAutoDailyPacing=False,
        endDate=None,
        budget=None,
        targetBid=None,
        maxBid=None,
        monthlyPacing=None,
        dailyPacing=None,
    )
    assert test_new_auction_lineitem is not None
    result = do_something_with_lineitem(test_new_auction_lineitem)
    assert result is not None

    testClass = TestClass()
    assert testClass is not None
    result = testClass._run(test_new_auction_lineitem)
    assert result is not None
