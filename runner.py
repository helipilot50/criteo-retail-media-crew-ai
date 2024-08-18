from tools.auth import AuthTool
from tools.accounts import AccountsTool
from tools.brands import BrandsTool
from tools.retailers import RetailersTool

auth = AuthTool()

auth_response = auth._run()
# print("auth response", auth_response)
token = auth_response['access_token']


accounts_tool = AccountsTool(token=token)
retailers_tool = RetailersTool(token=token)
brands_tool = BrandsTool(token=token)

my_accounts = accounts_tool._run()
print("my accounts", my_accounts)

my_retailers = retailers_tool._run("26")
print("my retailers", my_retailers)

my_brands = brands_tool._run("26")
print("my brands", my_brands)
