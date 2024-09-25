def attrubtes_only(li):
    return li["attributes"]


def flatten(element):
    flat = element["attributes"]
    flat["id"] = element["id"]
    # print(f"{element["type"]} flat:", flat)
    return flat

