import requests
import json
import os

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from crewai_tools import BaseTool


class SearchTools:
    """
    A set of seatch tools to search the internet, Instagram, LinkedIn, etc.
    """

    @tool("search internet")
    def search_internet(query: str) -> str:
        """
        Use this tool to search the internet for information. This tools returns 5 results from Google search engine.
        """
        return SearchTools.search(query)

    @tool("search instagram")
    def search_instagram(query: str) -> str:
        """
        Use this tool to search Instagram. This tools returns 5 results from Instagram pages.
        """
        return SearchTools.search(f"site:instagram.com {query}", limit=5)

    @tool("search linkedin")
    def search_linkedin(query: str) -> str:
        """
        Use this tool to search LinkedIn. This tools returns 5 results from LinkedIn pages.
        """
        return SearchTools.search(f"site:linkedin.com {query}", limit=5)

    @tool("open page")
    def open_page(url: str) -> str:
        """
        Use this tool to open a webpage and get the content.
        """
        loader = WebBaseLoader(url)
        return loader.load()

    def search(query, limit=5):

        url = "https://google.serper.dev/search"
        payload = json.dumps(
            {
                "q": query,
                "num": limit,
            }
        )
        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()["organic"]

        string = []
        for result in results:
            string.append(
                f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n"
            )

        return f"Search results for '{query}':\n\n" + "\n".join(string)


class InternetSearch(BaseTool):
    name: str = "Search the internet"
    description: str = "Search the internet for information."

    def _run(self, query: str):
        return SearchTools().search_internet(query)
