from typing import List
from crewai_tools import BaseTool
from part_3.tools.access import get_token
import requests
import os

base_url_env = os.environ["RETAIL_MEDIA_API_URL"]

def get_apikey():
    key = os.environ["RAPID_API_KEY"]
    print("api key is: ", key)
    return key


class ConcertsForArtistTool(BaseTool):
    """
    Calls the Concerts API and returns the Concerts for a given artist by the artist {id}
    """

    name: str = "Concerts API Caller"
    description: str = (
        "Calls the Concerts REST API and returns the Concerts for a given artist by the artist id "
    )

    def _run(self, artistName: str, page: int = 1):
        url = "https://concerts-artists-events-tracker.p.rapidapi.com/artist"

        params = {"name": artistName, "page": str(page)}

        headers = {
            "x-rapidapi-key": get_apikey(),
            "x-rapidapi-host": "concerts-artists-events-tracker.p.rapidapi.com",
        }

        response = requests.get(url=url, headers=headers, params=params)

        return response.json()

class NewCampaignForArtist(BaseTool):
    name: str = "New Campaign  for a concert tour",
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



        

