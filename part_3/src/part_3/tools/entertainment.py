from typing import List
from datetime import date, datetime
from crewai_tools import BaseTool
from part_3.models.campaign import (
    CampaignType,
    ClickAttributionWindow,
    NewCampaign,
    ViewAttributionWindow,
)
from part_3.models.concert import Concert
from part_3.models.lineitem import (
    LineitemBidStrategy,
    LineitemStatus,
    NewAuctionLineitem,
)
from part_3.tools.campaigns import NewCampaignTool
from part_3.tools.lineitems import NewAuctionLineitemTool


class NewCampaignForConcertTourTool(BaseTool):
    name: str = ("Campaign for concert tour",)
    description: str = """
        Creates a campaign and lineitems for the Concert tour
    """

    def __init__(self):
        self.newCampaignTool = NewCampaignTool()
        self.newAuctionLineitemTool = NewAuctionLineitemTool()

    def _run(
        self,
        artistName: str,
        year: str,
        budget: float,
        campaignStart: date,
        campaignEnd: date,
        pacing: float,
        accountId: str,
        concerts: List[Concert],
    ):

        time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Create campaign
        newCampaign = NewCampaign(
            name=f"{artistName} {year} Tour {time_stamp}",
            startDate=campaignStart,
            endDate=campaignEnd,
            budget=budget,
            type=CampaignType.auction,
            monthlyPacing=pacing,
            isAutoDailyPacing=False,
            clickAttributionWindow=ClickAttributionWindow.thirtyDays,
            viewAttributionWindow=ViewAttributionWindow.thirtyDays,
            clickAttributionScope="sameSkuCategory",
            viewAttributionScope="sameSkuCategory",
        )

        createdCampaign = self.newCampaignTool._run(
            accountId=accountId, campaign=newCampaign
        )

        # Create lineitems

        lineitems: List[NewAuctionLineitem] = []

        for concert in concerts:

            try:
                newLineitem = NewAuctionLineitem(
                    name=f"{artistName} {year} {concert.name} {time_stamp}",
                    startDate=campaignStart,
                    endDate=concert.date,
                    status=LineitemStatus.paused,
                    budget=concert.digitalAdvertisingBudget,
                    isAutoDailyPacing=False,
                    bidStrategy=LineitemBidStrategy.conversion,
                )

                createdLineitem = self.newAuctionLineitemTool._run(
                    campaignId=createdCampaign.id,
                    lineitem=newLineitem,
                )
                lineitems.append(createdLineitem)
            except Exception as e:
                print(f"Failed to create lineitem for concert {concert.name}: {e}")

        return {
            "campaign": createdCampaign,
            "lineitems": lineitems,
        }
