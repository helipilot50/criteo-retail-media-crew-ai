import json
from part_3.models.campaign import (
    CampaignStatus,
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

# from part_3.tools.entertainment import NewCampaignForConcertTourTool
from part_3.tools.lineitems import AuctionLineitemsTool, NewAuctionLineitemTool
from part_3.tools.utils import flatten
from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import AccountsCampaignsTool, NewCampaignTool
from crewai_tools import (
    FileWriterTool,
)
from datetime import date, datetime


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

    campaign = NewCampaign(
        name="Jimmy Carr Concert Tour 2030 "
        + current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        startDate="2030-01-01",
        endDate="2030-12-31",
        status=CampaignStatus.inactive,
        budget=1280000,
        isAutoDailyPacing=False,
        type=CampaignType.auction,
        clickAttributionWindow=ClickAttributionWindow.thirtyDays,
        viewAttributionWindow=ViewAttributionWindow.thirtyDays,
        clickAttributionScope=ClickAttributionScope.sameSkuCategory,
        viewAttributionScope=ViewAttributionScope.sameSkuCategory,
    )
    assert campaign is not None

    theCampaign = newCampaign._run(accountId=account_id, campaign=campaign)
    assert theCampaign is not None
    print("theNewCampaign --> ", theCampaign)

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_new_campaign_{theCampaign.id}.json",
        content=theCampaign.model_dump_json(indent=2),
        overwrite=True,
    )

    for i in range(1, 25):
        current_datetime = datetime.now()
        lineitemInput = NewAuctionLineitem(
            name="Jimmy Carr Concert Tour 2030 - Open Auction Lineitem "
            + current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            + " - "
            + str(i),  # name must be unique across the campaign
            startDate="2030-01-01",
            targetRetailerId="906",
            endDate="2030-12-31",
            status=LineitemStatus.paused,
            budget=1.00,
            targetBid=5,
            maxBid=5,
            monthlyPacing=50,
            dailyPacing=5,
            isAutoDailyPacing=False,
            bidStrategy=LineitemBidStrategy.conversion,
        )
        newAuctionLineitemResult = newAuctionLineitem._run(
            campaignId=theCampaign.id,
            lineitem=lineitemInput,
        )
        assert newAuctionLineitemResult is not None

    campainLineitemsResult = campainLineitems._run(campaignId=theCampaign.id)
    assert campainLineitemsResult is not None
    assert campainLineitemsResult["data"] is not None
    lineitems = list(map(flatten, campainLineitemsResult["data"]))
    assert len(lineitems) > 0
    fileWriter._run(
        directory="output",
        filename=f"test_{theCampaign.id}_lineitems.json",
        content=json.dumps(lineitems, indent=2),
        overwrite=True,
    )


# def test_new_campaign_for_concert_tour():
#     newTourTool = NewCampaignForConsertTourTool()
#     fileWriterTool = FileWriterTool()

#     results = newTourTool._run(
#         artistName="Jimmy Carr",
#         year="2030",
#         budget=1280000,
#         campaignStart=date(2030, 1, 1),
#         campaignEnd=date(2030, 12, 31),
#         pacing=500,
#         account=4,
#         concerts=[
#             dict(
#                 name="London",
#                 date=date(2030, 1, 1),
#                 digitalAdvertisingBudget=1000,
#             ),
#             dict(
#                 name="Manchester",
#                 date=date(2030, 1, 2),
#                 digitalAdvertisingBudget=1000,
#             ),
#             dict(
#                 name="Birmingham",
#                 date=date(2030, 1, 3),
#                 digitalAdvertisingBudget=1000,
#             ),
#         ],
#     )
#     assert results is not None

#     fileWriterTool._run(
#         directory="output",
#         filename=f"test_tour_{results["campaign"].id}_campaign.json",
#         content=json.dumps(results["campaign"], indent=2),
#         overwrite=True,
#     )
#     fileWriterTool._run(
#         directory="output",
#         filename=f"test_tour_{results["campaign"].id}_lineitems.json",
#         content=json.dumps(results["lineitems"], indent=2),
#         overwrite=True,
#     )
