from crewai_tools import BaseTool

import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class PreferredLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media preferred Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization
    """

    name: str = "Retail Media preferred Lineitems  API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the preferred Lineitems for a campaign using the  campaign {id}"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, campaignId: str):
        """
        Fetches the Retail Media preferred Lineitems for campaign by {campaignId} and returns relevant results
        """
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request(
            "GET",
            f"{self.base_url}campaigns/{campaignId}/preferred-line-items",
            headers=headers,
        )
        return response.json()


class AuctionLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media auction Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization
    """

    name: str = "Retail Media auction Lineitems API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the auction Lineitems for a campaign using the campaign {id}"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, campaignId: str):
        """
        Fetches the Retail Media auction Lineitems for campaign by {campaignId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request(
            "GET",
            f"{self.base_url}campaigns/{campaignId}/auction-line-items",
            headers=headers,
        )
        return response.json()


class AccountLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media account Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization
    """

    name: str = "Retail Media Account Lineitems API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the account Lineitems"
    )
    base_url: str = base_url_env
    token: str

    def _run(self, accountId: str):
        """
        Fetches the Retail Media account Lineitems for account by {accountId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request(
            "GET", f"{self.base_url}accounts/{accountId}/line-items", headers=headers
        )
        return response.json()
