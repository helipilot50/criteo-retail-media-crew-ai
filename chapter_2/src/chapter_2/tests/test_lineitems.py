

from chapter_2.tests.utils import fetchToken
from chapter_2.tools.accounts import AccountsTool
from chapter_2.tools.campaigns import CampaignsTool
from chapter_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool


def test_lineitems():
    token = fetchToken()
    assert token is not None

    accounts = AccountsTool(token=token)
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result['data'] is not None
    assert len(accounts_api_result['data']) > 0

    account_id = accounts_api_result['data'][0]['id']
    assert account_id is not None

    campaigns = CampaignsTool(token=token)
    campaigns_api_result = campaigns._run(accountId=account_id)
    assert campaigns_api_result is not None
    assert campaigns_api_result['data'] is not None
    assert len(campaigns_api_result['data']) > 0
    campaign_list = campaigns_api_result['data']
    preferred_campaign_id = next(x for x in campaign_list if x['attributes']['type'] == 'preferred')['id']

    preferred = PreferredLineitemsTool(token=token)
    preferred_api_result = preferred._run(campaignId=preferred_campaign_id)
    # print(preferred_api_result)
    assert preferred_api_result is not None
    assert preferred_api_result['data'] is not None
    data = preferred_api_result['data']
    meta_data = preferred_api_result['metadata']
    assert len(data) <= meta_data['totalItemsAcrossAllPages']

    auction_campaign_id = next(x for x in campaign_list if x['attributes']['type'] == 'auction')['id']
    auction = AuctionLineitemsTool(token=token)
    auction_api_result = auction._run(campaignId=auction_campaign_id)
    # print(auction_api_result)
    assert auction_api_result is not None
    assert auction_api_result['data'] is not None
    data = auction_api_result['data']
    meta_data = auction_api_result['metadata']
    assert len(data) <= meta_data['totalItemsAcrossAllPages']
    

