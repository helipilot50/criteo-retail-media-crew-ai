from typing import Type, Any
from crewai_tools import BaseTool, FileWriterTool, tool
from part_2.models.campaign import Campaign, CampaignList, NewCampaign
from part_2.tools.utils import flatten
from part_2.tools.access import get_token
import requests
import os
import json
from pydantic import BaseModel


base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


@tool("Campaigns for Account")
def campaigns_for_account_with_budget(
    accountId: str,
    pageIndex: int,  # = 0,
    pageSize: int,  # = 100,
    # withBudget: bool = False,
) -> CampaignList:
    """Calls the Retail Media REST API and returns the  campaigns for account id.
    Parameters:
    - 'pageIndex' a zero based page index
    - pageSize is 100 by default
    """
    fw = FileWriterTool()
    headers = {"Authorization": "Bearer " + get_token()}
    params = {"pageIndex": pageIndex, "pageSize": pageSize}
    url = f"{base_url_env}accounts/{accountId}/campaigns"
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
    )
    if response.status_code != 200:
        raise Exception("[Campaigns for Account] error:", response.json())

    response_body = response.json()
    if response_body is None or "data" not in response_body:
        return []
    the_campaigns = CampaignList(
        totalItems=response_body["metadata"]["totalItemsAcrossAllPages"]
    )

    for campaign_element in response_body["data"]:
        flat = flatten(campaign_element)
        # print("flat campaign --> ", flat)
        campaign = Campaign(**flat)
        # if withBudget:
        if campaign.budget is not None and campaign.budget > 0:
            the_campaigns.campaigns.append(campaign)
        # else:
        #     the_campaigns.campaigns.append(campaign)

    fw._run(
        directory="output",
        filename=f"debug_{accountId}_campaigns_{pageIndex}_{pageSize}.json",
        content=json.dumps(the_campaigns.model_dump(), indent=2),
        overwrite=True,
    )
    return the_campaigns


@tool("Campaign Tool")
def fetch_campaign(campaignId: str) -> Campaign:
    """
    Fetch a single Campaign by campaignId
    """
    headers = {"Authorization": "Bearer " + get_token()}
    response = requests.get(
        url=f"{base_url_env}campaigns/{campaignId}",
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception("[Campaign Tool] error:", response.json())
    theCampaign = Campaign(**flatten(response.json()["data"]))
    return theCampaign


@tool("New Campaign Tool")
def new_campaign(accountId: str, campaign: NewCampaign) -> Campaign:
    """Create  a campaign for an account using {account_id} and NewCampaign object.
    Example input for new Campaign:
    {
        "name": "{artist_name} Concert Tour {year}",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31",
        "budget": 1280000,
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
    """

    body = dict(
        data=dict(
            type="NewCampaign",
            attributes=campaign.model_dump(),
        ),
    )
    headers = {"Authorization": "Bearer " + get_token()}
    response = requests.post(
        url=f"{base_url_env}accounts/{accountId}/campaigns",
        headers=headers,
        json=body,
    )
    if response.status_code != 201:
        raise Exception("[New Campaign Tool] error:", response.json())
    data = response.json()["data"]
    flat = flatten(data)
    theCampaign = Campaign(**flat)

    return theCampaign
