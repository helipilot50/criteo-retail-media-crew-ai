import json
import os
from functools import reduce
from collections import defaultdict
from crewai_tools import FileWriterTool

from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import CampaignsTool
from part_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool

from part_2.tests.utils import (
    attrubtes_only,
    auction,
    budget,
    date,
    preferred,
    short_date,
)
from part_2.tools.charts import BarChartTool


def reduce_lineitems(auction_lineitems, preferred_lineitems):
    #  reduce values to year-month

    # Function to reduce the list
    def reducer_auction(acc, item):
        date = short_date(item["startDate"])
        value = budget(item)
        acc[date]["auction"] += value
        return acc

    def reducer_preferred(acc, item):
        date = short_date(item["startDate"])
        value = budget(item)
        acc[date]["preferred"] += value
        return acc

    # Using reduce to accumulate budgets by date
    result = reduce(
        reducer_auction,
        auction_lineitems,
        defaultdict(lambda: {"auction": 0, "preferred": 0}),
    )
    # print("result", result)
    result = reduce(reducer_preferred, preferred_lineitems, result)
    # print("result", result)
    return result


def test_analytics_bar_chart():

    # tools
    accounts = AccountsTool()
    campaigns = CampaignsTool()
    auction_li = AuctionLineitemsTool()
    preferred_li = PreferredLineitemsTool()
    fileWriter = FileWriterTool()

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

        # preferred
        preferred_api_result = preferred_li._run(campaignId=campaign_id)
        if preferred_api_result is not None:
            if "data" in preferred_api_result and len(preferred_api_result["data"]) > 0:
                lineitems = preferred_api_result["data"]
                preferred_lineitems.extend(map(attrubtes_only, lineitems))

        # auction
        auction_api_result = auction_li._run(campaignId=campaign_id)
        if auction_api_result is not None:
            if "data" in auction_api_result and len(auction_api_result["data"]) > 0:
                lineitems = auction_api_result["data"]
                auction_lineitems.extend(map(attrubtes_only, lineitems))

    reduced_lineitems = reduce_lineitems(auction_lineitems, preferred_lineitems)

    chart_data = [
        {
            "date": item[0],
            "auction": item[1]["auction"],
            "preferred": item[1]["preferred"],
        }
        for item in reduced_lineitems.items()
    ]
    fileWriter._run(directory='output', filename='test_lineitems_chart_data.json', content=json.dumps(chart_data), overwrite=True)
    

    file_name = "test_lineitem_bar_chart.png"
    if os.path.exists(f"output/{file_name}"):
        os.remove(f"output/{file_name}")

    dates = list(map(date, chart_data))
    auction_money = list(map(auction, chart_data))
    preferred_money = list(map(preferred, chart_data))

    bar = BarChartTool()
    chart = bar._run(
        categories=dates,
        values=[auction_money, preferred_money],
        x_label="Date",
        y_label="Budget",
        labels=["Auction", "Preferred"],
        title="Test Bar Chart",
        path="output",
        file_name=file_name,
    )
    assert os.path.exists(f"output/{file_name}")
    assert chart is not None
