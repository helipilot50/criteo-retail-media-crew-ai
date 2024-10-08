from pydantic import BaseModel


def attrubtes_only(li):
    return li["attributes"]


def flatten(element):
    flat = element["attributes"]
    flat["id"] = element["id"]
    # print(f"{element["type"]} flat:", flat)
    return flat


def pydantic_to_json(pydantic_obj: BaseModel) -> dict:
    return pydantic_obj.model_dump()
