from database import db_Session
import core
import utils
import json


def get_system_result(input_facts: dict):
    core_object = core.Core(db_Session)
    init_validation_result = core_object.validate_rules_with_facts()
    if not init_validation_result["status"] == "success":
        return init_validation_result
    init_validation_result = core_object.declare_multiply_facts(input_facts)
    if not init_validation_result["status"] == "success":
        return init_validation_result
    core_object.start()
    # print(core_object.rules_activated)

    updated_dict = core_object.facts
    # Находим ключи, которые есть в updated_dict, но отсутствуют в test_input
    added_keys = updated_dict.keys() - input_facts.keys()
    # Формируем словарь только с добавленными элементами
    added_facts = {key: updated_dict[key] for key in added_keys}

    __result = {
        "status": "success",
        "facts": added_facts,
        "rules":  [rule for rule in core_object.rules_activated if rule["rule_type"] != "Tech"]
    }

    # __result = {
    #     "status": "success",
    #     "facts": core_object.facts,
    #     "rules":  core_object.rules_activated
    # }
    return __result


def add_fact(fact: dict):
    core_object = core.Core(db_Session)
    return core_object.add_fact(fact)


def add_rule(rule: dict):
    core_object = core.Core(db_Session)
    return core_object.add_rule(rule)


test_input = {
    "depositCount": 1,
    "emplBank": False,
    "cusPassStoplist": False,
    "cusFIODRStoplist": False,
    "cusAddressStoplist": False,
    "cusMobPhoneStoplist": False,
    # "cusImpression": "Negative"
}
result = get_system_result(test_input)


# result = add_fact({
#     "FACT_NAME": "testfact",
#     "FACT_TYPE": "text",
#     "COMMENT": "xxxxx",
#     # "DEFAULT_VALUE": "Positive"
# })


# result = add_rule({
#     "RULE_NAME": "R005",
#     "RULE_LHS": [
#         {
#             "LHS_FACT_NAME": "cusImpression",
#             "LHS_OP": "eq",
#             "LHS_VALUE": "Negative"
#         },
#         # {
#         #     "LHS_FACT_NAME": "Segment",
#         #     "LHS_OP": "ne",
#         #     "LHS_VALUE": "NTB"
#         # }
#     ],
#     # "RULE_RHS": {
#     #   "RHS_FACT_NAME": "Segment",
#     #   "RHS_FACT_VALUE": "EXIST"
#     # },
#     "RULE_TYPE": "R",
#     "COMMENT": "Впечатление об участинке - негативное",
#     "PRIORITY": 1,
# })


print(json.dumps(result, indent=2, ensure_ascii=False))