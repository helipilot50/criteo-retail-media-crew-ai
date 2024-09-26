import json
from part_3.models.campaign import (
    CampaignType,
    ClickAttributionScope,
    ClickAttributionWindow,
    NewCampaign,
    ViewAttributionScope,
    ViewAttributionWindow,
)
from part_3.models.lineitem import (
    LineitemBidStrategy,
    LineitemStatus,
    NewAuctionLineitem,
)
from part_3.tools.lineitems import AuctionLineitemsTool, NewAuctionLineitemTool
from part_3.tools.utils import flatten
from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import AccountsCampaignsTool, NewCampaignTool
from crewai_tools import (
    FileWriterTool,
)
from datetime import datetime


def first_account():
    accounts = AccountsTool()
    accountListData = accounts._run()
    assert accountListData is not None
    assert len(accountListData) > 0
    assert "data" in accountListData
    accountList = list(map(flatten, accountListData["data"]))
    assert accountList is not None
    assert len(accountList) > 0
    return accountList[0]


def test_campaigns():
    # tools
    campaigns = AccountsCampaignsTool()
    fileWriter = FileWriterTool()

    account = first_account()
    account_id = account["id"]
    assert account_id is not None

    campaigns_api_result = campaigns._run(
        accountId=account_id, pageIndex=1, pageSize=1000
    )
    totalItems = campaigns_api_result["metadata"]["totalItemsAcrossAllPages"]
    print("totalItems --> ", totalItems)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    campaignsList = list(map(flatten, campaigns_api_result["data"]))
    assert len(campaignsList) > 0

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_campaigns.json",
        content=json.dumps(campaignsList, indent=2),
        overwrite=True,
    )


def test_new_campaign():
    # tools
    newCampaign = NewCampaignTool()
    fileWriter = FileWriterTool()
    newAuctionLineitem = NewAuctionLineitemTool()
    campainLineitems = AuctionLineitemsTool()

    account = first_account()
    account_id = account["id"]
    assert account_id is not None

    current_datetime = datetime.now()

    campaign = dict(
        name="Jimmy Carr Concert Tour 2030 "
        + current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        startDate="2030-01-01",
        endDate="2030-12-31",
        budget=1280000,
        isAutoDailyPacing=False,
        type=CampaignType.auction,
        clickAttributionWindow=ClickAttributionWindow.thirtyD,
        viewAttributionWindow=ViewAttributionWindow.none,
        clickAttributionScope=ClickAttributionScope.sameSkuCategory,
        viewAttributionScope=ViewAttributionScope.sameSkuCategory,
    )
    assert campaign is not None

    newCampaign = newCampaign._run(accountId=account_id, campaign=campaign)
    assert newCampaign is not None

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_new_campaign_{newCampaign.id}.json",
        content=json.dumps(newCampaign.model_dump_json(), indent=2),
        overwrite=True,
    )

    for i in range(1, 25):
        current_datetime = datetime.now()
        newAuctionLineitemResult = newAuctionLineitem._run(
            campaignId=newCampaign.id,
            lineitem=dict(
                name="Jimmy Carr Concert Tour 2030 - Open Auction Lineitem "
                + current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                + " - "
                + str(i),  # name must be unique across the campaign
                status=LineitemStatus.paused,
                targetRetailerId="1106",
                budget=500,
                startDate="2030-10-1",
                endDate="2030-12-31",
                bidStrategy=LineitemBidStrategy.conversion,
                targetBid=1.0,
            ),
        )
        assert newAuctionLineitemResult is not None

    campainLineitemsResult = campainLineitems._run(campaignId=newCampaign.id)
    assert campainLineitemsResult is not None
    assert campainLineitemsResult["data"] is not None
    lineitems = list(map(flatten, campainLineitemsResult["data"]))
    assert len(lineitems) > 0
    fileWriter._run(
        directory="output",
        filename=f"test_{newCampaign.id}_lineitems.json",
        content=json.dumps(lineitems, indent=2),
        overwrite=True,
    )
