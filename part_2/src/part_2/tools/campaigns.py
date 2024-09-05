from crewai_tools import BaseTool

import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class CampaignsTool(BaseTool):
    """
    Used to fetch the Retail Media campaigns and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
        token (str): The token for authorization.
    """

    name: str = "Retail Media Campaigns API Caller"
    description: str = (
        "Calls the Retail Media  REST API and returns the Campaigns for an account by the  account {id} "
    )
    base_url: str = base_url_env
    token: str

    def _run(self, accountId: str):
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request(
            "GET", f"{self.base_url}accounts/{accountId}/campaigns", headers=headers
        )
        return response.json()
