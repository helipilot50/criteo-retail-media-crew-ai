from crewai_tools import BaseTool

import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']

class CampaignsList(BaseTool):
    name: str = "Retail Media Campaigns API Caller"
    description: str = "Calls the Retail Media  REST API and returns the Campaigns accessable to the account manager"
    base_url:str = base_url_env
    token:str
    
    def _run(self, accountId:str) :
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/campaigns", headers=headers)
        return response.json()