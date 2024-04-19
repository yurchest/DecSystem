from database import db_Session
import core
import utils

core = core.Core(db_Session)
core.declare_fact("x", 5)
core.declare_fact("y", "5")
print(core.facts)
core.start()

print(f"Сработавшие правила: {core.rules_activated}")

utils.out_to_json(core.rules)
core.add_rule({
    "RULE_NAME": "Rule_5",
    "RULE_LHS": [
        {
            "LHS_FACT_NAME": "x",
            "LHS_OP": "lt",
            "LHS_VALUE": 100.0
        },
        {
            "LHS_FACT_NAME": "y",
            "LHS_OP": "lt",
            "LHS_VALUE": 100.0
        }
    ],
    "RULE_RHS": {
        "RHS_FACT_NAME": "y",
        "RHS_FACT_VALUE": 1.0
    },
    "COMMENT": None,
    "ADD_DATE": None
})
