import json
from part_3.tests import test_accounts
from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import AccountsCampaignsTool, NewCampaign, NewCampaignTool
from crewai_tools import (
    FileWriterTool,
)
from part_3.tools.utils import flattern


def first_account():
    accounts = AccountsTool()
    accountListData = accounts._run()
    assert accountListData is not None
    assert len(accountListData) > 0
    assert "data" in accountListData
    accountList = list(map(flattern, accountListData["data"]))
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
    # todo
    # if totalItems > 500:
    #     pageIndex = totalItems % 500
    #     campaigns_api_result = campaigns._run(
    #         accountId=account_id, pageIndex=pageIndex, pageSize=500
    #     )
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    campaignsList = list(map(flattern, campaigns_api_result["data"]))
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

    account = first_account()
    account_id = account["id"]
    assert account_id is not None

    campaign = NewCampaign(
        name="Jimmy Carr Concert Tour 2030",
        startDate="2030-01-01",
        endDate="2030-12-31",
        budget=1280000,
        monthlyPacing=500,
        dailyBudget=10,
        isAutoDailyPacing=False,
        dailyPacing=10,
        type="auction",
        clickAttributionWindow="30D",
        viewAttributionWindow="None",
        clickAttributionScope="sameSkuCategory",
        viewAttributionScope="sameSkuCategory",
    )

    newCampaignResult = newCampaign._run(accountId=account_id, campaign=campaign)
    print("newCampaignResult --> ", newCampaignResult)
    assert newCampaignResult is not None
    assert newCampaignResult["data"] is not None
    data = newCampaignResult["data"]

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_new_campaign.json",
        content=json.dumps(data, indent=2),
        overwrite=True,
    )
