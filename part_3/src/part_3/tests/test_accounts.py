import json
from part_3.tools.accounts import AccountsTool, BrandsTool, RetailersTool
from crewai_tools import (
    FileWriterTool,
)
from part_3.tools.utils import flatten



def test_accounts():

    accounts = AccountsTool()
    fileWriter = FileWriterTool()
    accountList = accounts._run()
    assert accountList is not None
    assert len(accountList) > 0
    fileWriter._run(
        directory="output",
        filename=f"test_accounts.json",
        content=json.dumps([acc.model_dump() for acc in accountList], indent=2),
        overwrite=True,
    )
    return accountList


def test_accounts_brands():

    fileWriter = FileWriterTool()
    accountList = test_accounts()

    account_id = accountList[0].id
    assert account_id is not None

    brands = BrandsTool()
    brands_list = brands._run(accountId=account_id)
    assert brands_list is not None
    assert len(brands_list) > 0
    print("brands_list --> ", brands_list)
    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_brands.json",
        overwrite=True,
        content=json.dumps([acc.model_dump() for acc in brands_list], indent=2),
    )


def test_accounts_retailers():

    fileWriter = FileWriterTool()
    retailers = RetailersTool()

    accountList = test_accounts()
    assert accountList is not None
    assert len(accountList) > 0

    account_id = accountList[0].id
    assert account_id is not None

    retailers_list = retailers._run(accountId=account_id)
    assert retailers_list is not None
    assert len(retailers_list) > 0
    print("retailers_list --> ", retailers_list)

    fileWriter._run(
        directory="output",
        filename=f"test_account_{account_id}_retailers.json",
        overwrite=True,
        content=json.dumps([acc.model_dump() for acc in retailers_list], indent=2),
    )



