import os
import json

output_directory = "output"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)


def full_file_path(file_name):
    return f"{output_directory}/{file_name}"


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


def auction(li):
    return li["auction"]


def preferred(li):
    return li["preferred"]


def money(li):
    return li["budget"]


def short_date(date: str):
    return date[:7]
