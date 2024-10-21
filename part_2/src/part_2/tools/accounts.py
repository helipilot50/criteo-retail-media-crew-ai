from typing import Any
from crewai_tools import BaseTool
from part_2.tools.utils import flatten
from part_2.models.account import Account
from part_2.tools.access import get_token
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
    
    def _run(self, pageIndex:int=0, pageSize:int=25):
        """Useful to fetch my Retail Media acounts and return relevant results"""

        url = base_url_env + 'accounts'
        authHeader:str = "Bearer " + get_token()
        headers = {
            "Authorization": authHeader
        }
        params = {"pageIndex":  pageIndex, "pageSize": pageSize}
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("[AccountsTool] error:", response.json())
        response_body = response.json()
        if response_body is None or "data" not in response_body:
            return []
        the_accounts: list[Account] = []
        for account_element in response_body["data"]:
            flat = flatten(account_element)
            # print("flat account --> ", flat)
            account = Account(**flat)
            the_accounts.append(account)
        return the_accounts

    

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
    
    def _run(self, accountId:str, pageIndex:int=0, pageSize:int=25):
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        } 
        params = {"pageIndex":  pageIndex, "pageSize": pageSize}
        response = requests.get(url=f"{self.base_url}accounts/{accountId}/brands", headers=headers, params=params)
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
    
    def _run(self, accountId:str, pageIndex:int=0, pageSize:int=25):
        headers =  {
            'Authorization': 'Bearer ' + get_token()
        }   
        params = {"pageIndex":  pageIndex, "pageSize": pageSize} 
        response = requests.get(url=f"{self.base_url}accounts/{accountId}/retailers", headers=headers, params=params)
        return response.json()
    

# choosers
def choose_account():
    accounts = AccountsTool()._run()
    print("\nPlease select an account:")
    for i, account in enumerate(accounts, 1):
        print(f"{i}. {account.name}")

    while True:
        try:
            choice = input(f"Enter the number of the account (default is 1): ")
            if choice == "" or choice == "1":
                return accounts[0]
            choice = int(choice)
            if 1 <= choice <= len(accounts):
                return accounts[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(accounts)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

