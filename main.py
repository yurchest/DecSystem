from database import db_Session
import core
import utils

core = core.Core(db_Session)
core.declare_fact("applFaFlag", "True")
core.declare_fact("cusAge", 19)
# core.declare_fact("y", "5")

print(core.facts)
core.start()

print("----------------------------------------")
print(f"Сработавшие правила: {core.rules_activated}")
print(core.facts)

# core.add_fact({
#     "FACT_NAME": "cusAge1",
#     "FACT_TYPE": "number",
#     "COMMENT": "Возраст",
#     # "DEFAULT_VALUE": "Accept"
# })
#
#
# utils.out_to_json(core.rules)
# core.add_rule({
#     "RULE_NAME": "Rule_Age_2",
#     "RULE_LHS": [
#         {
#             "LHS_FACT_NAME": "cusAge",
#             "LHS_OP": "lt",
#             "LHS_VALUE": 20
#         }
#     ],
#     "RULE_RHS": {
#         "RHS_FACT_NAME": "DECISION_RESULT",
#         "RHS_FACT_VALUE": "Reject"
#     },
#     "COMMENT": "Отсечение по возрасту",
#     "PRIORITY": 3,
# })
