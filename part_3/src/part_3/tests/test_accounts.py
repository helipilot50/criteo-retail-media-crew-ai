from part_3.tests.utils import  write_data
from part_3.tools.accounts import AccountsTool, BrandsTool, RetailersTool


def test_accounts():


    accounts = AccountsTool()
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    data = accounts_api_result["data"]
    write_data(data, "test_accounts.json")


def test_accounts_brands():


    accounts = AccountsTool()
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    brands = BrandsTool()
    brands_api_result = brands._run(accountId=account_id)
    assert brands_api_result is not None
    assert brands_api_result["data"] is not None
    assert len(brands_api_result["data"]) > 0
    data = brands_api_result["data"]
    write_data(data, "test_account_brands.json")


def test_accounts_retailers():


    accounts = AccountsTool()
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    retailers = RetailersTool()
    retailers_api_result = retailers._run(accountId=account_id)
    assert retailers_api_result is not None
    assert retailers_api_result["data"] is not None
    assert len(retailers_api_result["data"]) > 0
    data = retailers_api_result["data"]
    write_data(data, "test_account_retailers.json")
