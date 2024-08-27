from chapter_2.tests.utils import fetchToken
from chapter_2.tools.accounts import AccountsTool, BrandsTool, RetailersTool
from chapter_2.tools.campaigns import CampaignsTool


def test_campaigns():

    token = fetchToken()
    assert token is not None

    accounts = AccountsTool(token=token)
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    campaigns = CampaignsTool(token=token)
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result["data"] is not None
    assert len(campaigns_api_result["data"]) > 0
    # campaign_list = campaigns_api_result["data"]
    # print("campaigns", campaign_list)
