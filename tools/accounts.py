from crewai_tools import BaseTool
import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']

class AccountsTool(BaseTool):
    name: str = "Retail Media Accounts API Caller"
    description: str = "Calls the Retail Media  REST API and returns the Accounts accessable to the account manager"
    base_url:str = base_url_env

    token:str
    
    def _run(self) :
        """Useful to fetch my Retail Media acounts and return relevant results"""
        authHeader:str = "Bearer " + self.token
        headers = {
            "Authorization": authHeader
        }
        response = requests.request('GET', self.base_url + 'accounts', headers=headers)
        return response.json()
    


class BrandsTool(BaseTool):
    name: str = "Retail Media Brands API Caller"
    description: str = "Calls the Retail Media REST API and returns the Brands accessable to the account manager."
    base_url:str = base_url_env
    token:str
    
    def _run(self, accountId):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        } 
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/brands", headers=headers)
        return response.json()
 
    
class RetailersTool(BaseTool):
    name: str = "Retail Media Retailers API Caller"
    description: str = "Calls the Retail Media REST API and returns the Retailer  accessable to the account manager."
    token:str
    base_url:str = base_url_env
    
    def _run(self, accountId):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }    
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/retailers", headers=headers)
        return response.json()