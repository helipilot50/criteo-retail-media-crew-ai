import requests
import os
from crewai_tools import BaseTool
from cachetools import cached, TTLCache



class AuthTool(BaseTool):
    name: str = "Criteo Authentication API Caller"
    description: str = "Calls the Criteo Auth REST API and returns the access token."
    base_url: str = "https://api.criteo.com/oauth2/"

    def __init__(self):
        super().__init__()
        

    
    # @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def _run(self):

        clientId = os.environ['CRITEO_CLIENT_ID']
        clientSecret = os.environ['CRITEO_CLIENT_SECRET'];

        print("client id", clientId)
        print("client secret", clientSecret)


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': clientId,
            'client_secret': clientSecret,
            'grant_type': 'client_credentials'
        }
        
        response = requests.request("POST", self.base_url + "token", headers=headers, data=data)
        # print("response status: ",response.status_code)
        return response.json()


