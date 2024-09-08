import requests
import os
from crewai_tools import BaseTool
import time

class AuthTool(BaseTool):
    name: str = "Criteo Authentication API Caller"
    description: str = "Calls the Criteo Auth REST API and returns the access token."
    base_url: str = "https://api.criteo.com/oauth2/"

    def _run(self):

        clientId = os.environ["CRITEO_CLIENT_ID"]
        clientSecret = os.environ["CRITEO_CLIENT_SECRET"]

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "client_id": clientId,
            "client_secret": clientSecret,
            "grant_type": "client_credentials",
        }

        response = requests.request(
            "POST", self.base_url + "token", headers=headers, data=data
        )
        return response.json()

class Cache:
    def __init__(self, expiration_time):
        self.expiration_time = expiration_time
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = (value, time.time())

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.expiration_time:
                # print("Token Cache hit")
                return value
            else:
                del self.cache[key]  # Remove expired entry
                # print("Token Cache miss")
                auth = AuthTool()
                auth_response = auth._run()
                token = auth_response["access_token"]
                self.set("token", token)
                return token
        else:
            # print("Token Cache miss")
            auth = AuthTool()
            auth_response = auth._run()
            token = auth_response["access_token"]
            self.set("token", token)

        return token
    
tokenCache = Cache(expiration_time=890)  # Cache entries expire just less that 15 mins

def get_token():
    token = tokenCache.get("token")
    return token
