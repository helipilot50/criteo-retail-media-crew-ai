from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import CampaignsTool
from part_3.tests.utils import fetchToken
from part_3.tests.utils import write_data

from part_3.tools.analytics import CampaignAnalyticsTool


def test_create_impressions_report():
    token = fetchToken()
    assert token is not None

    # tools
    accounts = AccountsTool(token=token)
    campaigns = CampaignsTool(token=token)

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
    campaign_ids = [campaign["id"] for campaign in campaign_list]

    impressions_tool = CampaignAnalyticsTool(token=token)
    impressions_api_result = impressions_tool._run(
        campaignIds=campaign_ids, startDate="2020-01-01", endDate="2020-12-31"
    )
    assert impressions_api_result is not None
    data = impressions_api_result["data"]
    assert data is not None
    write_data(data, "test_impressions.json")
