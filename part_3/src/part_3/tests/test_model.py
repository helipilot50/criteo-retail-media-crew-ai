from part_3.models.lineitem import (
    NewAuctionLineitem,
)


def test_new_auction_lineitem():
    test_new_auction_lineitem = NewAuctionLineitem(
        name="test",
        startDate="2022-01-01",
        status="active",
        targetRetailerId="test",
        bidStrategy="clicks",
    )
    assert test_new_auction_lineitem is not None
