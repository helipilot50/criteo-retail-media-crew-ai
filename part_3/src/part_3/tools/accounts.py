from typing import Any
from crewai_tools import BaseTool

from part_3.tools.access import get_token
import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class AccountsTool(BaseTool):
    """
    Useful to fetch my Retail Media accounts and return relevant results.
    Attributes:
        name (str): The name of the tool ("Retail Media Accounts API Caller").
        description (str): The description of the tool ("Calls the Retail Media REST API and returns the Accounts accessible to the account manager").
        token (str): The token for authentication.
    Methods:
        _run(): Fetches the Retail Media accounts and returns the relevant results.
    """

    name: str = "Fetch Accounts Tool"
    description: str = (
        "Fetch the Accounts accessable to the account manager"
    )
    

    def _run(self, pageIndex: int = 0, pageSize: int = 25):
        """Useful to fetch my Retail Media acounts and return relevant results"""

        url = base_url_env + "accounts"
        authHeader: str = "Bearer " + get_token()
        headers = {"Authorization": authHeader}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(url=url, headers=headers, params=params)
        # print("account response:", response.json)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch Accounts, Error: {response.status_code} - {response.text}, {response.url}"
            )

        return response.json()


class BrandsTool(BaseTool):
    """
    Calls the Retail Media REST API and returns the Brands accessible to the account manager.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization.
    Methods:
        _run(accountId: str) -> dict: Calls the API and returns the Brands accessible to the specified account.
    """

    name: str = "Retail Media Brands API Caller"
    description: str = (
        "Calls the Retail Media REST API and returns the Brands accessable to the account manager."
    )
    

    def _run(self, accountId: str, pageIndex: int = 0, pageSize: int = 25):
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}accounts/{accountId}/brands",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch Brands, Error: {response.status_code} - {response.text}, {response.url}"
            )

        return response.json()


class RetailersTool(BaseTool):
    """
    Calls the Retail Media REST API and returns the Retailer accessible to the account manager.
    Attributes:
        name (str): The name of the RetailersTool.
        description (str): The description of the RetailersTool.
        base_url (str): The base URL for the Retail Media REST API.
        token (str): The token for authorization.
    Methods:
        _run(accountId: str) -> dict: Calls the Retail Media REST API to retrieve the retailers accessible to the account manager.
    """

    name: str = "Retail Media Retailers API Caller"
    description: str = (
        "Calls the Retail Media REST API and returns the Retailer  accessable to the account manager."
    )
    

    def _run(self, accountId: str, pageIndex: int = 0, pageSize: int = 25):
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}accounts/{accountId}/retailers",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch Retailers, Error: {response.status_code} - {response.text}, {response.url}"
            )

        return response.json()


class BalancesTool(BaseTool):
    """
    Calls the Retail Media REST API and returns the balances for the account.
    Attributes:
        name (str): The name of the BalancesTool.
        description (str): The description of the BalancesTool.
        base_url (str): The base URL for the Retail Media REST API.
        token (str): The token for authorization.
    Methods:
        _run(accountId: str) -> dict: Calls the Retail Media REST API to retrieve the balances for the account.
    """

    name: str = "Retail Media Balances API Caller"
    description: str = (
        "Calls the Retail Media REST API and returns the balances for the account."
    )
    

    def _run(self, accountId: str):
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.get(
            url=f"{base_url_env}accounts/{accountId}/balances",
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch Balances, Error: {response.status_code} - {response.text}, {response.url}"
            )

        return response.json()
