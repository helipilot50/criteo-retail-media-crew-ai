from crewai_tools import BaseTool
import requests
import os


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
