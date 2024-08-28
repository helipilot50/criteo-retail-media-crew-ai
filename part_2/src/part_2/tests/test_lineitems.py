from part_2.tests.utils import attrubtes_only, fetchToken
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import CampaignsTool
from part_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool


def test_lineitems():
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
    all_lineitems = []
    for target_campaign in campaign_list:
        campaign_id = target_campaign["id"]
        # print("id", campaign_id)

        # preferred
        preferred_api_result = preferred._run(campaignId=campaign_id)
        if preferred_api_result is not None:
            if "data" in preferred_api_result and len(preferred_api_result["data"]) > 0:
                lineitems = auction_api_result["data"]
                all_lineitems.extend(map(attrubtes_only, lineitems))

        # auction
        auction_api_result = auction._run(campaignId=campaign_id)
        if auction_api_result is not None:
            if "data" in auction_api_result and len(auction_api_result["data"]) > 0:
                lineitems = auction_api_result["data"]
                all_lineitems.extend(map(attrubtes_only, lineitems))

    assert len(all_lineitems) > 0
