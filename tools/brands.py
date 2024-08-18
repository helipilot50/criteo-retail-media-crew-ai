from crewai_tools import BaseTool
import requests


class BrandsTool(BaseTool):
    name: str = "Retail Media Retailers API Caller"
    description: str = "Calls the Retail Media Retailer REST API and returns the response."
    base_url: str = "https://api.criteo.com/2024-01/retail-media/"
    token:str
    
    def _run(self, accountId):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        } 
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/brands", headers=headers)
        return response.json()
