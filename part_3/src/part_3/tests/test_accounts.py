import json
from part_3.tools.accounts import AccountsTool, BrandsTool, RetailersTool
from crewai_tools import (
    FileWriterTool,
    FileReadTool,
    DirectoryReadTool,
    DirectorySearchTool,
)


def test_accounts():

    accounts = AccountsTool()
    fileWriter = FileWriterTool()
    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    data = accounts_api_result["data"]
    fileWriter._run(
        directory="output",
        filename=f"test_accounts.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )


def test_accounts_brands():

    accounts = AccountsTool()
    fileWriter = FileWriterTool()
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

    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    retailers_api_result = retailers._run(accountId=account_id)
    assert retailers_api_result is not None
    assert retailers_api_result["data"] is not None
    assert len(retailers_api_result["data"]) > 0
    data = retailers_api_result["data"]
    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_retailers.json",
        overwrite=True,
        content=json.dumps(data, indent=2),
    )
