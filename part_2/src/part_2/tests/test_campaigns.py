import json
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import CampaignsTool
from crewai_tools import FileWriterTool, FileReadTool, DirectoryReadTool, DirectorySearchTool


def test_campaigns():
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
    data = campaigns_api_result["data"]
    
    fileWriter._run(directory='output', filename=f'test_{account_id}_campaigns.json', content=json.dumps(data), overwrite=True)
    

