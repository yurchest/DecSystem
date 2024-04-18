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
    elif fact_type == "bool" and isinstance(value, int):
        return True
    else:
        return False
