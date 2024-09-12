import json
import os
import time
from functools import reduce
from collections import defaultdict
from crewai_tools import FileWriterTool
from crewai_tools import (
    FileWriterTool,
    FileReadTool,
    DirectoryReadTool,
    DirectorySearchTool,
)

from part_3.tools.accounts import AccountsTool, RetailersTool
from part_3.tools.campaigns import AccountsCampaignsTool, CampaignTool, NewCampaignTool
from part_3.tools.lineitems import (
    AuctionLineitemsTool,
    NewAuctionLineitemTool,
    PreferredLineitemsTool,
)
from datetime import datetime, timedelta


def test_new_campaign():
    # tools
    newCampaign = NewCampaignTool()
    accounts = AccountsTool()
    campaign = CampaignTool()
    fileWriter = FileWriterTool()

    # fetch accounts for the user
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    account_id = accounts_api_result["data"][0]["id"]  # get the first account
    assert account_id is not None

    # create a new campaign
    currentdate = time.strftime("%Y-%m-%d")
    currenttime = time.strftime("%H:%M:%S")
    campaign_name = "CrewAI Test Campaign " + currentdate + " " + currenttime

    # calculate the end date as 2 months after the start date
    start_date = datetime.strptime(currentdate, "%Y-%m-%d")
    end_date = start_date + timedelta(days=60)
    end_date_str = end_date.strftime("%Y-%m-%d")

    campaign_attributes = {
        "name": campaign_name,
        "accountId": account_id,
        "startDate": currentdate,
        "endDate": end_date_str,
        "budget": 1000,
        "monthlyPacing": 500,
        "dailyBudget": 10,
        "isAutoDailyPacing": False,
        "dailyPacing": 10,
        "type": "auction",
        "clickAttributionWindow": "30D",
        "viewAttributionWindow": "None",
        "clickAttributionScope": "sameSkuCategory",
        "viewAttributionScope": "sameSkuCategory",
    }

    # create a new campaign
    campaign_api_result = newCampaign._run(
        accountId=account_id, campaign=campaign_attributes
    )
    assert campaign_api_result is not None
    assert campaign_api_result["data"] is not None
    data = campaign_api_result["data"]
    assert campaign_api_result["data"]["id"] is not None
    new_campaign_id = campaign_api_result["data"]["id"]

    fileWriter._run(
        directory="output",
        filename=f"test_new_campaign_{new_campaign_id}.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )

    campaign_result_check = campaign._run(campaignId=new_campaign_id)
    assert campaign_result_check is not None
    assert campaign_result_check["data"] is not None
    check_data = campaign_result_check["data"]
    assert check_data["id"] == new_campaign_id
    return check_data


def test_new_lineitems_5():
    # tools
    fileWriter = FileWriterTool()
    new_auction_lineitem = NewAuctionLineitemTool()
    campaign_lineitems = AuctionLineitemsTool()
    retailers = RetailersTool()

    new_campaign = test_new_campaign()

    retailer_list = retailers._run(accountId=new_campaign["attributes"]["accountId"])[
        "data"
    ]
    assert retailer_list is not None
    assert len(retailer_list) > 4

    assert new_campaign is not None
    assert new_campaign["id"] is not None
    new_campaign_id = new_campaign["id"]

    currentdate = time.strftime("%Y-%m-%d")
    # create 5 new auction lineitems
    for i in range(5):
        # calculate the end date as 2 months after the start date
        start_date = datetime.strptime(currentdate, "%Y-%m-%d")
        end_date = start_date + timedelta(days=60)
        end_date_str = end_date.strftime("%Y-%m-%d")
        lineitem_name = f"Lineitem {i+1} for Campaign {new_campaign_id}"
        lineitem_attributes = {
            "name": lineitem_name,
            "campaignId": new_campaign_id,
            "status": "paused",
            "targetRetailerId": retailer_list[i]["id"],
            "budget": 50,
            "startDate": currentdate,
            "endDate": end_date_str,
            "bidStrategy": "conversion",
            "targetBid": 1.0,
        }
        lineitem_api_result = new_auction_lineitem._run(
            campaignId=new_campaign_id, lineitem=lineitem_attributes
        )
        assert lineitem_api_result is not None
        fileWriter._run(
            directory="output",
            filename=f"test_lineitem_api_result_{i}.json",
            overwrite=True,
            content=json.dumps(lineitem_api_result, indent=2),
        )

        assert lineitem_api_result["data"] is not None
        lineitem_data = lineitem_api_result["data"]
        assert lineitem_data["id"] is not None
        lineitem_id = lineitem_data["id"]

        fileWriter._run(
            directory="output",
            filename=f"test_new_lineitem_{lineitem_id}.json",
            overwrite=True,
            content=json.dumps(lineitem_data, indent=2),
        )

    new_lneitems = campaign_lineitems._run(campaignId=new_campaign_id)
    assert new_lneitems is not None
    assert new_lneitems["data"] is not None
    assert len(new_lneitems["data"]) == 5

    fileWriter._run(
        directory="output",
        filename=f"test_new_lineitems_for_campaign_{new_campaign_id}.json",
        overwrite=True,
        content=json.dumps(new_lneitems["data"], indent=2),
    )
