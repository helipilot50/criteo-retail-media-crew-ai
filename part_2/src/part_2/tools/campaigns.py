from typing import Optional
from crewai_tools import BaseTool, FileWriterTool
from part_2.models.campaign import Campaign, CampaignList, NewCampaign
from part_2.tools.utils import flatten
from part_2.tools.access import get_token
import requests
import os
import json


base_url_env = os.environ["RETAIL_MEDIA_API_URL"]


class AccountCampaignsTool(BaseTool):
    """
    Used to fetch the Retail Media campaigns and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
    """

    name: str = "Campaigns List Tool"
    description: str = "fetches a list of  Campaigns for an account id"

    def _run(
        self,
        account_id: str,
        page_index: Optional[int] = 0,
        page_size: Optional[int] = 100,
        with_budget: Optional[bool] = False,
        # **kwargs,
    ) -> CampaignList:
        fw = FileWriterTool()
        headers = {"Authorization": "Bearer " + get_token()}
        # account_id = kwargs.get("account_id")
        # if "page_index" in kwargs:
        #     page_index = kwargs["page_index"] or 0
        # if "page_size" in kwargs:
        #     page_size = kwargs["page_size"] or 100
        # if "with_budget" in kwargs:
        #     with_budget = kwargs["with_budget"] or False
        params = {"pageIndex": page_index, "pageSize": page_size}
        response = requests.get(
            url=f"{base_url_env}accounts/{account_id}/campaigns",
            headers=headers,
            params=params,
        )
        if response.status_code != 200:
            # logger.log(
            #     "error", f"[AccountCampaignsTool] error: {response.json()}", color="red"
            # )
            raise Exception("[AccountCampaignsTool] error:", response.json())

        response_body = response.json()
        if response_body is None or "data" not in response_body:
            return []
        the_campaigns = CampaignList(
            totalItems=response_body["metadata"]["totalItemsAcrossAllPages"]
        )

        for campaign_element in response_body["data"]:
            flat = flatten(campaign_element)
            # print("flat campaign --> ", flat)
            campaign = Campaign(**flat)
            if with_budget:
                if campaign.budget is not None and campaign.budget > 0:
                    the_campaigns.campaigns.append(campaign)
            else:
                the_campaigns.campaigns.append(campaign)

        fw._run(
            directory="output",
            filename=f"t_{account_id}_campaigns_{page_index}_{page_size}.json",
            content=json.dumps(the_campaigns.model_dump(), indent=2),
            overwrite=True,
        )
        return the_campaigns


class CampaignTool(BaseTool):
    """
    operations on a single campaign
    """

    name: str = "Campaign Tool"
    description: str = "Fetch a single Campaign by id"

    def _run(self, campaignId: str) -> Campaign:
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.get(
            url=f"{base_url_env}campaigns/{campaignId}",
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception("[CampaignTool] error:", response.json())
        theCampaign = Campaign(**flatten(response.json()["data"]))
        return theCampaign


class NewCampaignTool(BaseTool):
    """
    Used to create a Retail Media campaign and return relevant results.
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        base_url (str): The base URL of the API.
    """

    name: str = "NewCampaignTool"
    description: str = (
        """Create  a campaign for an account using {account_id} and NewCampaign object.
        Example input for new Campaign:
        {
            "name": "{artist_name} Concert Tour {year}",
            "startDate": "2025-01-01",
            "endDate": "2025-12-31",
            "budget": 1280000,
            "monthlyPacing": 500,
            "dailyBudget": 10,
            "isAutoDailyPacing": False,
            "dailyPacing": 10,
            "type": "auction",
            "clickAttributionWindow": "30D",
            "viewAttributionWindow": "None",
            "clickAttributionScope": "sameSkuCategory",
            "viewAttributionScope": "sameSkuCategory",
        }
        """
    )

    def _run(self, accountId: str, campaign: NewCampaign) -> Campaign:
        logger = logging.getLogger("crewai_logger")
        logger.info(
            f"[NewCampaignTool] Calling API with accountId: {accountId} and campaign: {campaign}"
        )

        body = dict(
            data=dict(
                type="NewCampaign",
                attributes=campaign.model_dump(),
            ),
        )
        headers = {"Authorization": "Bearer " + get_token()}
        response = requests.post(
            url=f"{base_url_env}accounts/{accountId}/campaigns",
            headers=headers,
            json=body,
        )
        if response.status_code != 201:
            raise Exception("[NewCampaignTool] error:", response.json())
        data = response.json()["data"]
        flat = flatten(data)
        theCampaign = Campaign(**flat)
        logger.info(
            f"[NewCampaignTool] Campaign created {json.dumps(theCampaign.model_dump(), indent=2)}"
        )
        return theCampaign
