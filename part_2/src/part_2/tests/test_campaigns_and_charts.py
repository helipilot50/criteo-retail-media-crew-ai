import json
import os
from part_2.tools.charts import pie_chart_tool
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import campaigns_for_account_with_budget
from crewai_tools import FileWriterTool


def test_campaigns_pie_chart():
    # tools
    accounts = AccountsTool()
    fileWriter = FileWriterTool()

    accounts_result = accounts._run()
    assert accounts_result is not None
    assert len(accounts_result) > 0

    account_id = accounts_result[0].id
    assert account_id is not None

    the_campaigns = campaigns_for_account_with_budget._run(
        accountId=account_id, pageIndex=0, pageSize=100
    )
    assert the_campaigns is not None
    assert len(the_campaigns.campaigns) > 0

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_campaigns.json",
        content=json.dumps(the_campaigns.model_dump(), indent=2),
        overwrite=True,
    )

    assert os.path.exists(f"output/test_{account_id}_campaigns.json")

    campaigns_with_budget = list(
        filter(lambda x: x.budget is not None, the_campaigns.campaigns)
    )
    print("campaigns_with_budget", len(campaigns_with_budget))
    labels = list(map(lambda x: x.name, campaigns_with_budget))
    values = list(map(lambda x: x.budget, campaigns_with_budget))
    # create a pie chart
    chart = pie_chart_tool._run(
        values=values,
        labels=labels,
        title="Test Pie Chart",
        file_name="test_campaigns_pie_chart.png",
        path="output",
    )
    assert os.path.exists("output/test_campaigns_pie_chart.png")
    assert chart is not None
