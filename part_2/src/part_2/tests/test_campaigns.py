import json
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import AccountCampaignsTool
from crewai_tools import (
    FileWriterTool,
)


def test_campaigns():
    # tools
    accounts = AccountsTool()
    campaigns = AccountCampaignsTool()
    fileWriter = FileWriterTool()

    accounts_result = accounts._run()
    assert accounts_result is not None
    assert len(accounts_result) > 0

    account_id = accounts_result[0].id
    assert account_id is not None

    campaigns_tool_result = campaigns._run(
        account_id=account_id, page_index=0, page_size=1000
    )
    assert campaigns_tool_result is not None
    assert len(campaigns_tool_result.campaigns) > 0
    campaigns_tool_result_1 = campaigns._run(
        account_id=account_id,
        page_index=1,  # no page size
    )
    assert campaigns_tool_result_1 is not None

    campaigns_tool_result.campaigns.extend(campaigns_tool_result_1.campaigns)

    fileWriter._run(
        directory="output",
        filename=f"test_{account_id}_campaigns.json",
        content=json.dumps(campaigns_tool_result.model_dump(), indent=2),
        overwrite=True,
    )
