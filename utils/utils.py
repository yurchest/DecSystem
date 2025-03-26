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
    
# Функция для преобразования значения в нужный тип
def convert_type(value, target_type):
    if target_type == 'bool':
        return bool(int(value))  # '0' -> False, '1' -> True
    elif target_type == 'int':
        return int(value)
    elif target_type == 'float':
        return float(value)
    elif target_type == 'str':
        return str(value)
    else:
        return value  # Если тип неизвестен, оставляем как есть


def is_fact_type(value, fact_type: str) -> bool:
    if fact_type == "text" and isinstance(value, str):
        return True
    elif fact_type == "number" and isinstance(value, float):
        return True
    elif fact_type == "bool" and (isinstance(value, bool)):
        return True
    else:
        return False


def get_truth(fact_value, relate: str, value) -> bool:
    ops = {'gt': operator.gt,  # >
           'lt': operator.lt,  # <
           'ge': operator.ge,  # >=
           'le': operator.le,  # <=
           'eq': operator.eq,  # ==
           'ne': operator.ne}  # !=

    if relate not in ops:
        return False
    elif fact_value is None or value is None:
        return False
    else:
        return ops[relate](fact_value, value)


def out_to_json(dictionary: dict):
    with open("rules.json", "w") as outfile:
        json.dump(dictionary, outfile, indent=2, sort_keys=False)


def is_validated_schema(rule: dict, schema) -> bool:
    try:
        jsonschema.validate(instance=rule, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as ex:
        # print(ex)
        return False
        # exit(-1)  # TODO


def return_message(status: str, messages: list or None):
    return {
        "status": status,
        "messages": messages
    }
