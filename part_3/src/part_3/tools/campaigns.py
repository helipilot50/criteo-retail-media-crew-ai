from crewai_tools import BaseTool
from part_3.tools.access import get_token

import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']

class CampaignsTool(BaseTool):
    name: str = "Retail Media Campaigns API Caller"
    description: str = "Calls the Retail Media  REST API and returns the Campaigns accessable to the account manager"
    base_url:str = base_url_env
    
    def _run(self, accountId:str) :
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        }
        response = requests.get(url=f"{self.base_url}accounts/{accountId}/campaigns", headers=headers)
        return response.json()