from crewai_tools import BaseTool, FileWriterTool
from part_3.models.campaign import Campaign, CampaignList, NewCampaign
from part_3.tools.utils import flatten
from part_3.tools.access import get_token
import requests
import os
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
)
import json

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class AccountCampaignsTool(BaseTool):
    """
    Used to fetch the Retail Media campaigns and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Campaigns List Tool"
    description: str = "fetches a list of  Campaigns for an account id"

    def _run(
        self, accountId: str, pageIndex: int = 0, pageSize: int = 25
    ) -> CampaignList:
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}accounts/{accountId}/campaigns",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[AccountCampaignsTool] error:", response.json())

        response_body = response.json()
        if response_body is None or "data" not in response_body:
            return []
        the_campaigns = CampaignList(
            totalItems=response_body["metadata"]["totalItemsAcrossAllPages"]
        )

        for campaign_element in response_body["data"]:
            flat = flatten(campaign_element)
            print("flat campaign --> ", flat)
            campaign = Campaign(**flat)
            the_campaigns.campaigns.append(campaign)

        return the_campaigns


class CampaignTool(BaseTool):
    """
    operations on a single campaign
    """

    name: str = "Campaign Tool"
    description: str = "Fetch a single Campaign by id"

    def _run(self, campaignId: str) -> Campaign:
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.get(
            url=f"{base_url_env}campaigns/{campaignId}",
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception("[CampaignTool] error:", response.json())
        theCampaign = Campaign(**flatten(response.json()["data"]))
        return theCampaign


class NewCampaignTool(BaseTool):
    """
    Used to create a Retail Media campaign and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "NewCampaignTool"
    description: str = (
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
    )

    def _run(self, accountId: str, campaign: NewCampaign) -> Campaign:
        fileWriter = FileWriterTool()

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
            raise Exception("[NewCampaignTool] error:", response.json())
        data = response.json()["data"]
        flat = flatten(data)
        theCampaign = Campaign(**flat)
        fileWriter._run(
            content=json.dumps(theCampaign.model_dump(), indent=2),
            directory="output",
            filename=f"t_{theCampaign.id}_campaign.json",
            overwrite=True)
        return theCampaign
