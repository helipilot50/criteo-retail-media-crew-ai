import json
from part_3.tools.accounts import AccountsTool, BalancesTool, BrandsTool, RetailersTool
from crewai_tools import (
    FileWriterTool,
)
from part_3.tools.utils import flattern


def test_accounts():

    accounts = AccountsTool()
    fileWriter = FileWriterTool()
    accountListData = accounts._run()
    assert accountListData is not None
    assert len(accountListData) > 0
    assert "data" in accountListData
    accountList = list(map(flattern, accountListData["data"]))
    fileWriter._run(
        directory="output",
        filename=f"test_accounts.json",
        overwrite=True,
        content=json.dumps(accountList, indent=2),
    )
    return accountList


def test_accounts_brands():

    fileWriter = FileWriterTool()
    accountList = test_accounts()

    account_id = accountList[0]["id"]
    assert account_id is not None

    brands = BrandsTool()
    brands_api_result = brands._run(accountId=account_id)
    assert brands_api_result is not None
    assert brands_api_result["data"] is not None
    assert len(brands_api_result["data"]) > 0
    data = list(map(flattern, brands_api_result["data"]))
    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_brands.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )


def test_accounts_retailers():

    accounts = AccountsTool()
    fileWriter = FileWriterTool()
    retailers = RetailersTool()

    accountListData = accounts._run()
    assert accountListData is not None
    assert len(accountListData) > 0
    assert "data" in accountListData
    accountList = list(map(flattern, accountListData["data"]))

    account_id = accountList[0]["id"]
    assert account_id is not None

    retailers_api_result = retailers._run(accountId=account_id)
    assert retailers_api_result is not None
    assert retailers_api_result["data"] is not None
    assert len(retailers_api_result["data"]) > 0
    data = list(map(flattern, retailers_api_result["data"]))

    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_retailers.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )


def test_accounts_balances():
    fileWriter = FileWriterTool()
    balances = BalancesTool()

    accountList = test_accounts()

    account_id = accountList[0]["id"]
    assert account_id is not None

    balances_api_result = balances._run(accountId=account_id)
    assert balances_api_result is not None
    assert balances_api_result["data"] is not None
    data = list(map(flattern, balances_api_result["data"]))

    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_balances.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )
