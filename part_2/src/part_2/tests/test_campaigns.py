from part_2.tests.utils import  write_data
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import CampaignsTool


def test_campaigns():

    accounts = AccountsTool()
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    campaigns = CampaignsTool()
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    assert len(campaigns_api_result["data"]) > 0
    data = campaigns_api_result["data"]
    write_data(data, "test_campaigns.json")
