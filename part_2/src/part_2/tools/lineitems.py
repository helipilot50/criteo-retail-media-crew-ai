from crewai_tools import BaseTool

import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']

class PreferredLineitemsTool(BaseTool):
    name: str = "Retail Media preferred Lineitems  API Caller"
    description: str = "Calls the Retail Media  REST API and returns the preferred Lineitems for a campaign"
    base_url:str = base_url_env
    token:str
    
    def _run(self, campaignId:str) :
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.request('GET', f"{self.base_url}campaigns/{campaignId}/preferred-line-items", headers=headers)
        return response.json()
    
class AuctionLineitemsTool(BaseTool):
    name: str = "Retail Media auction Lineitems API Caller"
    description: str = "Calls the Retail Media  REST API and returns the auction Lineitems for a campaign"
    base_url:str = base_url_env
    token:str
    
    def _run(self, campaignId:str) :
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.request('GET', f"{self.base_url}campaigns/{campaignId}/auction-line-items", headers=headers)
        return response.json()
    
class AccountLineitemsTool(BaseTool):
    name: str = "Retail Media Account Lineitems API Caller"
    description: str = "Calls the Retail Media  REST API and returns the account Lineitems"
    base_url:str = base_url_env
    token:str
    
    def _run(self, accountId:str) :
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/line-items", headers=headers)
        return response.json()