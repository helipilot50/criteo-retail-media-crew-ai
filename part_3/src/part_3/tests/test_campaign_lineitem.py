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

from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import CampaignsTool, NewCampaignTool
from part_3.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool
from datetime import datetime, timedelta


def test_new_campaign():
    # tools
    newCampaign = NewCampaignTool()
    accounts = AccountsTool()
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
    end_date = start_date + timedelta(days=120)
    end_date_str = end_date.strftime("%Y-%m-%d")

    campaign_attributes = {
        "name": campaign_name,
        "accountId": account_id,
        "startDate": currentdate,
        "endDate": end_date_str,
        "budget": 1000,
        "monthlyPacing": 500,
        "dailyBudget": 10,
        "dailyPacing": 10,
        "type": "auction",
        "clickAttributionWindow": "30D",
        "viewAttributionWindow": "None",
        "clickAttributionScope": "sameSkuCategory",
        "viewAttributionScope": "sameSkuCategory",
        "companyName": "CrewAI Test Company",
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
        filename=f"test_campaign_{new_campaign_id}.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )
