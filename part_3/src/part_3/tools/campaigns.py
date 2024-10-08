import datetime
from typing import Optional
from crewai_tools import BaseTool, FileWriterTool
import json
from part_3.models.campaign import Campaign, NewCampaign
from part_3.tools.utils import flatten
from pydantic import BaseModel
from part_3.tests.utils import attrubtes_only
from part_3.tools.access import get_token
import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class AccountsCampaignsTool(BaseTool):
    """
    Used to fetch the Retail Media campaigns and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization.
    """

    name: str = "Retail Media Campaigns API"
    description: str = (
        "Calls the Retail Media  REST API and returns the Campaigns for an account by the  account {id} "
    )
    base_url: str = base_url_env

    def _run(self, accountId: str, pageIndex: int = 0, pageSize: int = 25):
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{self.base_url}accounts/{accountId}/campaigns",
            headers=headers,
            params=params,
        )

        return response.json()


class CampaignTool(BaseTool):
    """
    operations on a single campaign
    """

    name: str = "SingleCampaignTool"
    description: str = (
        "Calls the Retail Media  REST API and returns a single Campaign by the  campaign {id} "
    )
    base_url: str = base_url_env

    def _run(self, campaignId: str) -> Campaign:
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.get(
            url=f"{self.base_url}campaigns/{campaignId}",
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception("CampaignTool error:", response.json())
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
    base_url: str = base_url_env

    def _run(self, accountId: str, campaign: NewCampaign) -> Campaign:
        fileWriter = FileWriterTool()
        fileWriter._run(
            directory="output",
            filename=f"new_campaign_object_t.json",
            content=json.dumps(campaign.model_dump_json(), indent=2),
            overwrite=True,
        )
        headers = {"Authorization": "Bearer " + get_token()}

        response = requests.post(
            url=f"{self.base_url}accounts/{accountId}/campaigns",
            headers=headers,
            json={
                "data": {
                    "type": "NewCampaign",
                    "attributes": campaign.model_dump_json(),
                },
            },
        )
        if response.status_code != 201:
            raise Exception("NewCampaignTool error:", response.json())
        data = response.json()["data"]
        flat = flatten(data)

        theCampaign = Campaign(**flat)
        fileWriter._run(
            directory="output",
            filename=f"new_campaign_{theCampaign.id}_created_t.json",
            content=json.dumps(theCampaign.model_dump_json, indent=2),
            overwrite=True,
        )
        return theCampaign
