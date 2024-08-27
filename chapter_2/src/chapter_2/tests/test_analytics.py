import os

from chapter_2.tools.accounts import AccountsTool
from chapter_2.tools.campaigns import CampaignsTool
from chapter_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool
from chapter_2.tests.utils import (
    attrubtes_only,
    budget,
    date,
    date_budget,
    fetchToken,
    money,
    start_date,
)
from chapter_2.tools.charts import BarChartTool


def test_analytics_bar_chart():
    token = fetchToken()
    assert token is not None

    # tools
    accounts = AccountsTool(token=token)
    campaigns = CampaignsTool(token=token)
    auction = AuctionLineitemsTool(token=token)
    preferred = PreferredLineitemsTool(token=token)

    # accounts
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    # campaigns for first account
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    assert len(campaigns_api_result["data"]) > 0
    campaign_list = campaigns_api_result["data"]

    # lineitems
    preferred_lineitems = []
    auction_lineitems = []
    for target_campaign in campaign_list:
        campaign_id = target_campaign["id"]
        # print("id", campaign_id)

        # preferred
        preferred_api_result = preferred._run(campaignId=campaign_id)
        if preferred_api_result is not None:
            if "data" in preferred_api_result and len(preferred_api_result["data"]) > 0:
                lineitems = auction_api_result["data"]
                preferred_lineitems.extend(map(attrubtes_only, lineitems))

        # auction
        auction_api_result = auction._run(campaignId=campaign_id)
        if auction_api_result is not None:
            if "data" in auction_api_result and len(auction_api_result["data"]) > 0:
                lineitems = auction_api_result["data"]
                auction_lineitems.extend(map(attrubtes_only, lineitems))
    ordered_auction_lineitems = sorted(
        auction_lineitems, key=lambda lineitem: lineitem["startDate"]
    )
    ordered_preferred_lineitems = sorted(
        preferred_lineitems, key=lambda lineitem: lineitem["startDate"]
    )

    auction_values = list(map(date_budget, ordered_auction_lineitems))
    print("auction values", auction_values)
    preferred_values = list(map(date_budget, ordered_preferred_lineitems))
    print("preferred values", preferred_values)

    output_directory = "output"
    file_name = output_directory + "/test_lineitem_bar_chart.png"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if os.path.exists(file_name):
        os.remove(file_name)

    dates = list(map(date, auction_values))
    print("dates", dates)
    auction_budgets = list(map(money, auction_values))
    print("auction budgets", auction_budgets)

    bar = BarChartTool()
    chart = bar._run(
        categories=[dates],
        values=[auction_budgets],
        x_label="Dates",
        y_label="Budget",
        labels=["Auction"],
        title="Lineitem Budgets",
        file_name=file_name,
    )
    assert os.path.exists(file_name)
    assert chart is not None
