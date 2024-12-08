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

    __result = {
        "status": "success",
        "facts": core_object.facts,
        "rules": list(core_object.rules_activated)
    }
    return __result


def add_fact(fact: dict):
    core_object = core.Core(db_Session)
    return core_object.add_fact(fact)


def add_rule(rule: dict):
    core_object = core.Core(db_Session)
    return core_object.add_rule(rule)


test_input = {
    "cusAge": "77",
    "applFaFlag": True,
    "cusDepositsCount": 5,
    "Salary": 2000

}
result = get_system_result(test_input)


# result = add_fact({
#     "FACT_NAME": "Salary",
#     "FACT_TYPE": "number",
#     "COMMENT": "Зарплата",
#     # "DEFAULT_VALUE": "Accept"
# })

#
# result = add_rule({
#     "RULE_NAME": "Test_Rule_2",
#     "RULE_LHS": [
#         {
#             "LHS_FACT_NAME": "Salary",
#             "LHS_OP": "lt",
#             "LHS_VALUE": 25000
#         }
#     ],
#     "RULE_RHS": {
#         "RHS_FACT_NAME": "DECISION_RESULT",
#         "RHS_FACT_VALUE": "Reject"
#     },
#     "COMMENT": "Отсечение по зарплате",
#     "PRIORITY": 3,
# })


print(json.dumps(result, indent=2, ensure_ascii=False))