import operator
import json
import jsonschema


def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_bool(value) -> bool:
    return True if value in ["True", "False"] else False


def str2bool(v):
    return v.lower() in ("true",)


def retype_fact_value(value, fact_type: str):
    if fact_type == "text":
        return str(value)
    elif fact_type == "number" and is_number(value):
        return float(value)
    elif fact_type == "bool" and is_bool(value):
        return str2bool(value)
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


def is_validated_schema(rule: dict, schema) -> bool:
    try:
        jsonschema.validate(instance=rule, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as ex:
        # print(ex)
        return False
        # exit(-1)  # TODO
