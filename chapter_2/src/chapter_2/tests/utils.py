from chapter_2.tools.auth import AuthTool


def fetchToken():
    auth = AuthTool()
    response = auth._run()
    return response["access_token"]


def attrubtes_only(li):
    return li["attributes"]


def start_date(li):
    return li["startDate"]


def end_date(li):
    return li["endDate"]


def budget(li):
    if li["budget"]:
        return li["budget"]
    else:
        return 0


def date_budget(li):
    return {"date": start_date(li), "budget": budget(li)}


def date(li):
    return li["date"]


def money(li):
    return li["budget"]
