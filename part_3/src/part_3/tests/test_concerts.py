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
from part_3.tools.entertainment import ConcertsForArtistTool
from part_3.tools.lineitems import (
    AuctionLineitemsTool,
    NewAuctionLineitemTool,
)
from datetime import datetime, timedelta


def test_artist_campaign():
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
    concerts_api_result = concerts._run(artistName=artistName, page=1)
    assert concerts_api_result is not None
    assert concerts_api_result["data"] is not None

    concerts = concerts_api_result["data"]
    if len(concerts) > 0:
        # write the concerts to a file
        fileWriter._run(
            directory="output",
            filename=f"test_concerts_{artistName}.json",
            overwrite=True,
            content=json.dumps(concerts_api_result, indent=2),
        )
    else:
        print("using dummy data")
        concerts = fileReader._run(
            directory="src/part_3/tools",
            filename="entertainment_response.json",
        )

    # create a new campaign for the artist
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
    campaign_name = f"CrewAI Test Campaign for {artistName} {currentdate} {currenttime}"

    # calculate the start date as today
    start_date = datetime.strptime(currentdate, "%Y-%m-%d")
    # calculate the end date as last concert date
    end_date = max(concerts, key=lambda x: x["endDate"])

    # print(f"The latest event is {latest_event['name']} on {latest_event['date'].strftime('%Y-%m-%d')}")

    # end_date = start_date + timedelta(days=60)
    # end_date_str = end_date.strftime("%Y-%m-%d")

    campaign_attributes = {
        "name": campaign_name,
        "accountId": account_id,
        "startDate": currentdate,
        "endDate": end_date,
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
        filename=f"test_new_campaign_{new_campaign_id}.json",
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

    currentdate = time.strftime("%Y-%m-%d")

    i = 0
    # create new auction lineitems based on the concert locations
    for concert in concerts:

        start_date = concert["endDate"] - timedelta(days=30)

        lineitem_attributes = {
            "name": concert["description"],
            "campaignId": new_campaign_id,
            "status": "paused",
            "targetRetailerId": retailer_list[i]["id"],
            "budget": 50,
            "startDate": start_date,
            "endDate": concert["endDate"],
            "bidStrategy": "conversion",
            "targetBid": 1.0,
        }
        lineitem_api_result = newAuctionLineitem._run(
            campaignId=new_campaign_id, lineitem=lineitem_attributes
        )
        assert lineitem_api_result is not None
        i += 1
        # fileWriter._run(
        #     directory="output",
        #     filename=f"test_lineitem_api_result_{i}.json",
        #     overwrite=True,
        #     content=json.dumps(lineitem_api_result, indent=2),
        # )

        assert lineitem_api_result["data"] is not None
        lineitem_data = lineitem_api_result["data"]
        assert lineitem_data["id"] is not None
        # lineitem_id = lineitem_data["id"]

        # fileWriter._run(
        #     directory="output",
        #     filename=f"test_new_lineitem_{lineitem_id}.json",
        #     overwrite=True,
        #     content=json.dumps(lineitem_data, indent=2),
        # )

    new_lneitems = campaignLineitems._run(campaignId=new_campaign_id)
    assert new_lneitems is not None
    assert new_lneitems["data"] is not None
    assert len(new_lneitems["data"]) == 5

    fileWriter._run(
        directory="output",
        filename=f"test_concert_campaign_{new_campaign_id}_lineitems.json",
        overwrite=True,
        content=json.dumps(new_lneitems["data"], indent=2),
    )
