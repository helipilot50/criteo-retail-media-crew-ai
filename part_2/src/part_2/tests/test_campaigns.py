import json
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import AccountCampaignsTool
from crewai_tools import FileWriterTool, FileReadTool, DirectoryReadTool, DirectorySearchTool


def test_campaigns():
    # tools
    accounts = AccountsTool()
    campaigns = AccountCampaignsTool()
    fileWriter = FileWriterTool()

    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    
    campaigns_tool_result = campaigns._run(accountId=account_id, pageIndex=0, pageSize=100)
    assert campaigns_tool_result is not None
    assert len(campaigns_tool_result.campaigns) > 0
    
    
    fileWriter._run(directory='output', filename=f'test_{account_id}_campaigns.json', content=json.dumps(campaigns_tool_result.model_dump(), indent=2), overwrite=True)
    

