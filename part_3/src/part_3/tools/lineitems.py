from crewai_tools import BaseTool
from part_3.tools.access import get_token
import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']

class PreferredLineitemsTool(BaseTool):
    name: str = "Retail Media preferred Lineitems  API Caller"
    description: str = "Calls the Retail Media  REST API and returns the preferred Lineitems for a campaign"
    base_url:str = base_url_env
    
    def _run(self, campaignId:str) :
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        }
        response = requests.get(url=f"{self.base_url}campaigns/{campaignId}/preferred-line-items", headers=headers)
        return response.json()
    
class AuctionLineitemsTool(BaseTool):
    name: str = "Retail Media Auction Lineitems t API Caller"
    description: str = "Calls the Retail Media  REST API and returns the auction Lineitems for a campaignr"
    base_url:str = base_url_env
    token:str
    
    def _run(self, campaignId:str) :
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        }
        response = requests.get(url=f"{self.base_url}campaigns/{campaignId}/auction-line-items", headers=headers)
        return response.json()
    
class AccountLineitemsTool(BaseTool):
    name: str = "Retail Media Account Lineitems API Caller"
    description: str = "Calls the Retail Media  REST API and returns the account Lineitems"
    base_url:str = base_url_env
    
    def _run(self, accountId:str) :
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        }
        response = requests.get(url=f"{self.base_url}accounts/{accountId}/line-items", headers=headers)
        return response.json()