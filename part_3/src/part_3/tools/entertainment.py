from typing import List
from crewai_tools import BaseTool
from part_3.tools.access import get_token
import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]

class NewCampaignForArtist(BaseTool):
    name: str = "New Campaign for a concert tour",
    description: str = """
        Creates a campaign and lineitems for the astist

    """
    base_url: str = base_url_env
    def _run(self, artistName, year, account, campaign: dict, lineitems: List):

        
        # Create campaign
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.post(
            url=f"{self.base_url}accounts/{account}/campaigns",
            headers=headers,
            json={
                "data": {"type": "Lineitem", "attributes": campaign},
            },
        )

        newCampaign = response.json()["data"]


        # Create lineitems

        headers = {"Authorization": "Bearer " + get_token()}
        for lineitem in lineitems:
            response = requests.post(
                url=f"{self.base_url}campaigns/{newCampaign["id"]}/auction-line-items",
                headers=headers,
                json={
                    "data": {
                        "type": "NewLineitems",
                        "attributes": lineitem,
                    }
                },
            )

        # fetch created campaign
        campaignResponse = requests.get(
            url=f"{self.base_url}campaigns/{newCampaign["id"]}",
            headers=headers,
        )

        # fetch created lineitems

        lineitemsResponse = requests.get(
            url=f"{self.base_url}campaigns/{newCampaign["id"]}/lineitems",
            headers=headers,
        )

        return {
            "campaign": campaignResponse.json(),
            "lineitems": lineitemsResponse.json(),
        }



        

