import datetime
from part_3.models.lineitem import (
    LineitemStatus,
    NewAuctionLineitem,
)
from crewai_tools import BaseTool


class TestClass(BaseTool):
    name: str = "A tool"
    description: str = "does stuff with lineitem"

    def _run(self, lineitem: NewAuctionLineitem):
        return do_something_with_lineitem(lineitem)


def do_something_with_lineitem(lineitem: NewAuctionLineitem) -> NewAuctionLineitem:
    return lineitem


def test_new_auction_lineitem():
    test_new_auction_lineitem = NewAuctionLineitem(
        name="test",
        startDate=datetime.date(2022, 1, 1),
        status=LineitemStatus.draft,
        targetRetailerId="test",
        bidStrategy="clicks",
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
