from crewai_tools import BaseTool

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

    name: str = "Retail Media Campaigns API Caller"
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


class CampaignTool:
    """
    operations on a single campaign
    """

    name: str = "Retail Media Single Campaign API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns a single Campaign by the  campaign {id} "
    )
    base_url: str = base_url_env

    def _run(self, campaignId: str):
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.get(
            url=f"{self.base_url}campaigns/{campaignId}",
            headers=headers,
        )

        return response.json()


class NewCampaignTool(BaseTool):
    """
    Used to create a Retail Media campaign and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media New Campaign API Caller"
    description: str = (
        "Calls the Retail Media  REST API and creates a campaign for an account by the  account {id}"
    )
    base_url: str = base_url_env
    # accounts/{accountId}/campaigns

    def _run(self, accountId: str, campaign: dict):
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.post(
            url=f"{self.base_url}accounts/{accountId}/campaigns",
            headers=headers,
            json={
                "data": {"type": "Lineitem", "attributes": campaign},
            },
        )

        return response.json()
