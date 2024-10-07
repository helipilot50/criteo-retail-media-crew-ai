import json
from crewai_tools import BaseTool

from part_3.models.lineitem import (
    AuctionLineitem,
    NewAuctionLineitem,
)
from part_3.tools.access import get_token
from part_3.tools.utils import flatten
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
    """

    name: str = "Retail Media preferred Lineitems  API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the preferred Lineitems for a campaign using the  campaign {id}"
    )
    base_url: str = base_url_env

    def _run(self, campaignId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media preferred Lineitems for campaign by {campaignId} and returns relevant results
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{self.base_url}campaigns/{campaignId}/preferred-line-items",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[PreferredLineitemsTool] error:", response.json())
        return response.json()


class AuctionLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media auction Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media auction Lineitems API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the auction Lineitems for a campaign using the campaign {id}"
    )
    base_url: str = base_url_env

    def _run(self, campaignId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media auction Lineitems for campaign by {campaignId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{self.base_url}campaigns/{campaignId}/auction-line-items",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[AuctionLineitemsTool] error:", response.json())
        return response.json()


class AccountLineitemsTool(BaseTool):
    """
    Used to fetch the Retail Media account Lineitems and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media Account Lineitems API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the account Lineitems"
    )
    base_url: str = base_url_env

    def _run(self, accountId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media account Lineitems for account by {accountId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{self.base_url}accounts/{accountId}/line-items",
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
        base_url (str): The base URL of the API.
    """

    name: str = "New Auction Lineitem API"
    description: str = (
        """
        Calls the Retail Media  REST API and creates a Open Auction Lineitem for a campaign by the campaign id.
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
    base_url: str = base_url_env

    def _run(self, campaignId: str, lineitem: NewAuctionLineitem):
        """
        Creates a Retail Media Auction Lineitem for campaign by {campaignId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        # json={
        #         "data": {"type": "NewCampaign", "attributes": campaign},
        #     },
        payload = {
            "data": {
                "type": f"{campaignId}",
                "attributes": lineitem,
            }
        }
        response = requests.post(
            url=f"{self.base_url}campaigns/{campaignId}/auction-line-items",
            json=payload,
            headers=headers,
            
        )
        if response.status_code != 201:
            print("[NewAuctionLineitemTool] errors:", response.json()["errors"])
            raise Exception("[NewAuctionLineitemTool] errors:", response.json()["errors"])
        data = response.json()["data"]
        flat = flatten(data)
        theLineitem = AuctionLineitem(**flat)
        return theLineitem


class NewPreferredLineitemTool(BaseTool):
    """
    Used to create a Retail Media Preferred Lineitem and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media New Preferred Lineitem API Caller"
    description: str = (
        "Calls the Retail Media  REST API and creates a preferred Lineitem for a campaign by the campaign {id}"
    )
    base_url: str = base_url_env

    def _run(self, campaignId: str, lineitem: dict):
        """
        Creates a Retail Media  Preferred Lineitem for campaign by {campaignId} and returns relevant results.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.post(
            url=f"{self.base_url}campaigns/{campaignId}/preferred-line-items",
            headers=headers,
            json=lineitem,
        )
        if response.status_code != 201:
            raise Exception("[NewPreferredLineitemTool] error:", response.json())
        return response.json()

class PromotedProducts(BaseTool):
    """
    Used to fetch the Retail Media Promoted Products  for a Lineitem and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "Retail Media Promoted Products API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the Promoted Products for a lineitem using the lineitem id"
    )
    base_url: str = base_url_env

    def _run(self, lineitemId: str, pageIndex: int = 0, pageSize: int = 25):
        """
        Fetches the Retail Media Promoted Products on the Lineitem.
        """
        headers = {"Authorization": "Bearer " + get_token()}
        params = {"pageIndex": pageIndex, "pageSize": pageSize}
        response = requests.get(
            url=f"{self.base_url}line-items/{lineitemId}/products",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            raise Exception("[PromotedProducts] error:", response.json())
        return response.json()



# class LineitemsT():
#     @tool("New auction lineitem")
#     def new_auction_lineitem(self, campaignId:str, lineitem: NewAuctionLineitem) -> AuctionLineitem:
#         """
#             Calls the Retail Media  REST API and creates a Open Auction Lineitem for a campaign by the campaign id.
#             Example input data for a new lineitem:
#             {
#                 "name": Taylor Swift 2025 - AccorHotels Arena Paris- 2025-05-20,
#                 "campaignId": "626444481539563520",
#                 "status": "paused",
#                 "targetRetailerId": "1106",
#                 "budget": 50,
#                 "startDate": "2025-10-1",
#                 "endDate": "2025-12-31",
#                 "bidStrategy": "conversion",
#                 "targetBid": 1.0,
#             }
#         """
#         headers = {"Authorization": "Bearer " + get_token()}
#         response = requests.post(
#             url=f"{base_url_env}campaigns/{campaignId}/auction-line-items",
#             headers=headers,
#             json={
#                 "data": {
#                     "type": "NewLineitems",
#                     "attributes": lineitem.model_dump_json(),
#                 }
#             },
#         )
#         if response.status_code != 201:
#             raise Exception("[NewAuctionLineitemTool] error:", response.json())
#         data = response.json()["data"]
#         flat = flatten(data)
#         theLineitem = AuctionLineitem(**flat)
#         return theLineitem