import os
import json
from part_1.tools.accounts import AccountsTool, BrandsTool, RetailersTool
from crewai_tools import (
    FileWriterTool,
    FileReadTool,
    DirectoryReadTool,
    DirectorySearchTool,
)

accounts = AccountsTool()
brands = BrandsTool()
fileWriter = FileWriterTool()
retailers = RetailersTool()


def test_accounts():

    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0
    data = accounts_api_result["data"]
    fileWriter._run(
        directory="output",
        filename=f"test_accounts.json",
        overwrite=True,
        content=json.dumps(data),
    )
    assert os.path.exists("output/test_accounts.json")


def test_accounts_brands():

    accounts_api_result = accounts._run()
    assert accounts_api_result is not None
    assert accounts_api_result["data"] is not None
    assert len(accounts_api_result["data"]) > 0

    account_id = accounts_api_result["data"][0]["id"]
    assert account_id is not None

    brands_api_result = brands._run(accountId=account_id)
    assert brands_api_result is not None
    assert brands_api_result["data"] is not None
    assert len(brands_api_result["data"]) > 0
    data = brands_api_result["data"]
    fileWriter._run(
        directory="output",
        filename=f"test_brands.json",
        overwrite=True,
        content=json.dumps(data),
    )
    assert os.path.exists("output/test_brands.json")


def test_accounts_retailers():

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
        filename=f"test_retailers.json",
        overwrite=True,
        content=json.dumps(data),
    )
    assert os.path.exists("output/test_retailers.json")
