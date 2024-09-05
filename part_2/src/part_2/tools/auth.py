import requests
import os
from crewai_tools import BaseTool


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
