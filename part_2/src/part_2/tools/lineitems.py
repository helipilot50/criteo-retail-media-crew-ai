import json
from crewai_tools import BaseTool
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
)

from part_2.models.lineitem import (
    AuctionLineitem,
    LineitemList,
    NewAuctionLineitem,
)
from part_2.tools.access import get_token
from part_2.tools.utils import flatten
import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class PreferredLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media preferred Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Preferred Lineitems Tool"
    description: str = (
        "Fetch a list of preferred Lineitems for a campaign id. This tool uses pageIndex and pageSize to paginate the results."
    )

    def _run(self, campaignId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media preferred Lineitems for campaign by {campaignId} and returns relevant results
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}campaigns/{campaignId}/preferred-line-items",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[PreferredLineitemsTool] error:", response.json())
        response_body = response.json()
        if response_body is None:
            return []
        return response_body


class AuctionLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media auction Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "AuctionLineitemsTool"
    description: str = (
        "Fetch a list of  auction Lineitems for a campaign id. This tool uses pageIndex and pageSize to paginate the results."
    )

    def _run(
        self, campaignId: str, pageIndex: int = 0, pageSize: int = 25
    ) -> list[AuctionLineitem]:
        """
        Fetches the Retail Media auction Lineitems for campaign by {campaignId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}campaigns/{campaignId}/auction-line-items",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[AuctionLineitemsTool] error:", response.json())

        response_body = response.json()
        if response_body is None or "data" not in response_body:
            return []

        lineitem_list = LineitemList(
            totalItems=response_body["metadata"]["totalItemsAcrossAllPages"]
        )
        for lineitem_element in response_body["data"]:
            flat = flatten(lineitem_element)
            lineitem_list.lineitems.append(AuctionLineitem(**flat))

        return lineitem_list


class AccountLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media account Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media Account Lineitems API Caller"
    description: str = "Fetch the account lineitems for account id"

    def _run(self, accountId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media account Lineitems for account id {accountId}.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}accounts/{accountId}/line-items",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[AccountLineitemsTool] error:", response.json())
        return response.json()


class NewAuctionLineitemTool(BaseTool):
    """
    Onsite Sponsored Products Line Items
    Used to create a Retail Media Auction Lineitem and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "NewAuctionLineitemTool"
    description: str = (
        """
        Creates a NewAuctionLineitem for a campaign id.
        Example input data for a new lineitem:
        {
            "name": Taylor Swift 2025 - AccorHotels Arena Paris- 2025-05-20,
            "campaignId": "626444481539563520",
            "status": "paused",
            "targetRetailerId": "1106",
            "budget": 50,
            "startDate": "2025-10-1",
            "endDate": "2025-12-31",
            "bidStrategy": "conversion",
            "targetBid": 1.0,
        }
        """
    )

    def _run(self, campaignId: str, lineitem: NewAuctionLineitem):
        """
        Creates an  Auction Lineitem for a campaign id
        """

        fileWriter = FileWriterTool()
        headers = {"Authorization": "Bearer " + get_token()}

        payload = dict(
            data=dict(type="NewAuctionLineitem", attributes=lineitem.model_dump())
        )
        response = requests.post(
            url=f"{base_url_env}campaigns/{campaignId}/auction-line-items",
            json=payload,
            headers=headers,
        )
        if response.status_code != 201:
            print("[NewAuctionLineitemTool] errors:", response.json()["errors"])
            raise Exception(
                "[NewAuctionLineitemTool] errors:", response.json()["errors"]
            )
        data = response.json()["data"]
        flat = flatten(data)
        theLineitem = AuctionLineitem(**flat)
        fileWriter._run(
            content=json.dumps(theLineitem.model_dump(), indent=2),
            directory="output",
            filename=f"t_{campaignId}_lineitem_{theLineitem.id}.json",
            overwrite=True
        )
        return theLineitem



class NewPreferredLineitemTool(BaseTool):
    """
    Used to create a Retail Media Preferred Lineitem and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "NewPreferredLineitemTool"
    description: str = "Creates a preferred Lineitem for a campaign id"

    def _run(self, campaignId: str, lineitem: dict):
        """
        Creates a Retail Media  Preferred Lineitem for campaign by {campaignId} and returns relevant results.
        """

        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.post(
            url=f"{base_url_env}campaigns/{campaignId}/preferred-line-items",
            headers=headers,
            json=lineitem,
        )
        if response.status_code != 201:
            print("[NewPreferredLineitemTool] errors:", response.json()["errors"])
            raise Exception("[NewPreferredLineitemTool] error:", response.json())

        return response.json()


class PromotedProducts(BaseTool):
    """
    Used to fetch the Retail Media Promoted Products  for a Lineitem and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Retail Media Promoted Products API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the Promoted Products for a lineitem using the lineitem id"
    )

    def _run(self, lineitemId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media Promoted Products on the Lineitem.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{base_url_env}line-items/{lineitemId}/products",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[PromotedProducts] error:", response.json())
        return response.json()
