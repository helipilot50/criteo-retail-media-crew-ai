from crewai_tools import BaseTool

import requests
import os

base_url_env = os.environ['RETAIL_MEDIA_API_URL']


class AccountsTool(BaseTool):
    """
    Useful to fetch my Retail Media accounts and return relevant results.
    Attributes:
        name (str): The name of the tool ("Retail Media Accounts API Caller").
        description (str): The description of the tool ("Calls the Retail Media REST API and returns the Accounts accessible to the account manager").
        base_url (str): The base URL for the API.
        token (str): The token for authentication.
    Methods:
        _run(): Fetches the Retail Media accounts and returns the relevant results.
    """
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
    """
    Calls the Retail Media REST API and returns the Brands accessible to the account manager.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization.
    Methods:
        _run(accountId: str) -> dict: Calls the API and returns the Brands accessible to the specified account.
    """
    name: str = "Retail Media Brands API Caller"
    description: str = "Calls the Retail Media REST API and returns the Brands accessable to the account manager."
    base_url:str = base_url_env
    token:str
    
    def _run(self, accountId:str):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        } 
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/brands", headers=headers)
        return response.json()
 
    
class RetailersTool(BaseTool):
    """
    Calls the Retail Media REST API and returns the Retailer accessible to the account manager.
    Attributes:
        name (str): The name of the RetailersTool.
        description (str): The description of the RetailersTool.
        base_url (str): The base URL for the Retail Media REST API.
        token (str): The token for authorization.
    Methods:
        _run(accountId: str) -> dict: Calls the Retail Media REST API to retrieve the retailers accessible to the account manager.
    """
    name: str = "Retail Media Retailers API Caller"
    description: str = "Calls the Retail Media REST API and returns the Retailer  accessable to the account manager."
    base_url:str = base_url_env
    token:str
    
    def _run(self, accountId:str):
        headers =  {
            'Authorization': 'Bearer ' + self.token
        }    
        response = requests.request('GET', f"{self.base_url}accounts/{accountId}/retailers", headers=headers)
        return response.json()
    
