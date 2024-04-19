import operator
import json
import jsonschema
from .config import ruleSchema


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_flag(num):
    if int(num) in [0, 1]:
        return True
    else:
        return False


def retype_fact_value(value, fact_type: str):
    if fact_type == "text":
        return str(value)
    elif fact_type == "number" and is_number(value):
        return float(value)
    elif fact_type == "flag" and is_flag(value):
        return int(value)
    else:
        return value


def is_fact_type(value, fact_type: str) -> bool:
    if fact_type == "text" and isinstance(value, str):
        return True
    elif fact_type == "number" and isinstance(value, float):
        return True
    elif fact_type == "bool" and isinstance(value, bool):
        return True
    else:
        return False


def get_truth(fact_value, relate: str, value) -> bool:
    ops = {'gt': operator.gt,  # >
           'lt': operator.lt,  # <
           'ge': operator.ge,  # >=
           'le': operator.le,  # <=
           'eq': operator.eq}  # ==

    if relate not in ops:
        return False
    elif fact_value is None or value is None:
        return False
    else:
        return ops[relate](fact_value, value)


def out_to_json(dict: dict):
    with open("rules.json", "w") as outfile:
        json.dump(dict, outfile, indent=2, sort_keys=False)


def is_validated_rule_schema(rule: dict) -> bool:
    try:
        jsonschema.validate(instance=rule, schema=ruleSchema)
        return True
    except jsonschema.exceptions.ValidationError as ex:
        print(ex)
        exit(-1)  # TODO
        return False
