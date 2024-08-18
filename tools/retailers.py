from crewai_tools import BaseTool
import requests


class RetailersTool(BaseTool):
    name: str = "Retail Media Retailers API Caller"
    description: str = "Calls the Retail Media Retailer REST API and returns the response."
    token:str
    base_url: str = "https://api.criteo.com/2024-01/retail-media/"
    
    def _run(self, accountId):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }    
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/retailers", headers=headers)
        return response.json()