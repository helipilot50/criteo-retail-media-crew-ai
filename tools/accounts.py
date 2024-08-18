from crewai_tools import BaseTool
import requests


class AccountsTool(BaseTool):
    name: str = "Retail Media Accounts API Caller"
    description: str = "Calls the Retail Media Accounts REST API and returns the response."
    base_url:str = "https://api.criteo.com/2024-01/retail-media/"

    token:str


    
    def _run(self) :
        """Useful to fetch my Retail Media acounts and return relevant results"""
        authHeader:str = "Bearer " + self.token
        headers = {
            "Authorization": authHeader
        }
        response = requests.request('GET', self.base_url + 'accounts', headers=headers)
        return response.json()
    

    
    
