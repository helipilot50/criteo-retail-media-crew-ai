import json
import os
import time
from functools import reduce
from collections import defaultdict
from typing import Any, List
from crewai_tools import FileWriterTool
from crewai_tools import (
    FileWriterTool,
    FileReadTool,
    DirectoryReadTool,
    DirectorySearchTool,
)

from part_3.tools.accounts import AccountsTool, RetailersTool
from part_3.tools.campaigns import AccountCampaignsTool, CampaignTool, NewCampaignTool
from part_3.tools.entertainment import ConcertsForArtistTool
from part_3.tools.lineitems import (
    AuctionLineitemsTool,
    NewAuctionLineitemTool,
)
from datetime import datetime, timedelta


def find_first_last_event(collection: List[Any]) -> Any:

    # Find the object with the latest startDate
    latest_object = max(collection, key=lambda x: x["endDate"])
    earliest_object = min(collection, key=lambda x: x["startDate"])

    return {"first": earliest_object, "last": latest_object}


def x_test_concert_dates():
    fileReader = FileReadTool()

    concerts_file = fileReader._run(
        file_path="./data/ed_sheeran_entertainment_venues.json",
    )
    assert concerts_file is not None

    concerts = json.loads(concerts_file)
    # print("concerts --> ", concerts)
    assert len(concerts) > 0
    first_last_event = find_first_last_event(concerts)
    assert first_last_event is not None
    assert "first" in first_last_event
    assert "last" in first_last_event
    # print("first_last_event --> ", first_last_event)


def x_test_concert_campaign():
    # tools
    concerts = ConcertsForArtistTool()
    fileWriter = FileWriterTool()
    fileReader = FileReadTool()
    accounts = AccountsTool()
    newAuctionLineitem = NewAuctionLineitemTool()
    campaignLineitems = AuctionLineitemsTool()
    newCampaign = NewCampaignTool()
    retailers = RetailersTool()

    artistName = "Ed Sheran"

    # fetch concerts for the artist
    # concerts_api_result = concerts._run(artistName=artistName, page=1)
    # assert concerts_api_result is not None
    # assert concerts_api_result["data"] is not None

    # concerts = concerts_api_result["data"]
    # if len(concerts) > 0:
    #     # write the concerts to a file
    #     fileWriter._run(
    #         directory="output",
    #         filename=f"test_concerts_{artistName}.json",
    #         overwrite=True,
    #         content=json.dumps(concerts_api_result, indent=2),
    #     )
    # else:
    print("using dummy data")
    concerts_file = fileReader._run(
        file_path="./data/ed_sheeran_entertainment_venues.json",
    )
    assert concerts_file is not None
    # print("concerts_file --> ", concerts_file)
    concerts = json.loads(concerts_file)
    # print("concerts --> ", concerts)

    # create a new campaign for the artist
    # fetch accounts for the user
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    account_id = accounts_api_result["data"][0]["id"]  # get the first account
    assert account_id is not None

    # create a new campaign
    current_datetime = datetime.now()
    current_date_str = current_datetime.strftime("%Y-%m-%d")
    current_date_8601 = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    currenttime = time.strftime("%H:%M:%S")
    campaign_name = (
        f"CrewAI Test Campaign for {artistName} {current_date_str} {currenttime}"
    )

    # calculate the start date as today
    start_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    # calculate the end date as last concert date
    events = find_first_last_event(concerts)
    last_event = events["last"]
    first_event = events["first"]

    campaign_attributes = {
        "name": campaign_name,
        "accountId": account_id,
        "startDate": first_event["startDate"],
        "endDate": last_event["endDate"],
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
    new_campaign = campaign_api_result["data"]

    fileWriter._run(
        directory="output",
        filename=f"test_{new_campaign_id}_new_concert_campaign_.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )

    # create a new auction line items for the campaign
    retailer_list = retailers._run(accountId=new_campaign["attributes"]["accountId"])[
        "data"
    ]
    assert retailer_list is not None
    assert len(retailer_list) > 4

    assert new_campaign is not None
    assert new_campaign["id"] is not None
    new_campaign_id = new_campaign["id"]

    current_date_str = time.strftime("%Y-%m-%d")

    i = 0
    total_retailers = len(retailer_list)
    # create new auction lineitems based on the concert locations
    for concert in concerts:

        lineitem_attributes = {
            "name": concert["description"],
            "campaignId": new_campaign_id,
            "status": "paused",
            "targetRetailerId": retailer_list[i]["id"],
            "budget": 50,
            "startDate": first_event["startDate"],
            "endDate": concert["endDate"],
            "bidStrategy": "conversion",
            "targetBid": 1.0,
        }
        i += 1
        if i >= total_retailers:
            i = 0
        try:
            lineitem_api_result = newAuctionLineitem._run(
                campaignId=new_campaign_id, lineitem=lineitem_attributes
            )
            # print("lineitem_api_result --> ", lineitem_api_result)
            assert lineitem_api_result is not None
            assert lineitem_api_result["data"] is not None
            lineitem_data = lineitem_api_result["data"]
            assert lineitem_data["id"] is not None
            lineitem_id = lineitem_data["id"]

            fileWriter._run(
                directory="output",
                filename=f"test_{new_campaign_id}_new_venue_lineitem_{lineitem_id}.json",
                overwrite=True,
                content=json.dumps(lineitem_data, indent=2),
            )
        except Exception as e:
            print("error --> ", e)

    new_lneitems = campaignLineitems._run(campaignId=new_campaign_id)
    assert new_lneitems is not None
    assert new_lneitems["data"] is not None
    fileWriter._run(
        directory="output",
        filename=f"test_{new_campaign_id}_concert_campaign_lineitems.json",
        overwrite=True,
        content=json.dumps(new_lneitems["data"], indent=2),
    )
    assert len(new_lneitems["data"]) > 0
