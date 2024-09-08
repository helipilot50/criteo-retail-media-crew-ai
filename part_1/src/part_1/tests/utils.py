from part_1.tools.auth import AuthTool


def fetchToken():
    auth = AuthTool()
    response = auth._run()
    print("response", response)
    return response["access_token"]
