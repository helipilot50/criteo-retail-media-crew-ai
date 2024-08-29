from part_3.tests.utils import fetchToken, write_data
from part_3.tools.accounts import AccountsTool, BrandsTool, RetailersTool


def test_accounts():

    token = fetchToken()
    assert token is not None

    accounts = AccountsTool(token=token)
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    data = accounts_api_result["data"]
    write_data(data, "test_accounts.json")


def test_accounts_brands():

    token = fetchToken()
    assert token is not None

    accounts = AccountsTool(token=token)
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    brands = BrandsTool(token=token)
    brands_api_result = brands._run(accountId=account_id)
    assert brands_api_result is not None
    assert brands_api_result["data"] is not None
    assert len(brands_api_result["data"]) > 0
    data = brands_api_result["data"]
    write_data(data, "test_account_brands.json")


def test_accounts_retailers():

    token = fetchToken()
    assert token is not None

    accounts = AccountsTool(token=token)
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    retailers = RetailersTool(token=token)
    retailers_api_result = retailers._run(accountId=account_id)
    assert retailers_api_result is not None
    assert retailers_api_result["data"] is not None
    assert len(retailers_api_result["data"]) > 0
    data = retailers_api_result["data"]
    write_data(data, "test_account_retailers.json")
