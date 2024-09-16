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
from part_2.tools.charts import BarChartTool, PieChartTool

def test_campaigns_budget_pie_chart():
    def campaign_name(campaign):
        return campaign["attributes"]["name"]
    
    def campaign_budget(campaign):
        if campaign["attributes"]["budget"]:
            return campaign["attributes"]["budget"]
        else:
            return 0.0
    
    # tools
    accounts = AccountsTool()
    campaigns = CampaignsTool()
    fileWriter = FileWriterTool()

    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    assert len(campaigns_api_result["data"]) > 0
    names = list(map(campaign_name, campaigns_api_result["data"]))
    budgets = list(map(campaign_budget, campaigns_api_result["data"]))

    file_name = "test_campaigns_budget_pie_chart.png"
    path = "output"

    if os.path.exists(f"{path}/{file_name}"):
        os.remove(f"{path}/{file_name}")

    pie = PieChartTool()
    chart = pie._run(
        values=budgets,
        labels=names,
        title=f"Test Campaigns budget Pie Chart for Account {account_id}",
        file_name=file_name,
        path=path,
    )
    assert os.path.exists(f"{path}/{file_name}")
    assert chart is not None

