ruleSchema = {
    "type": "object",
    "properties": {
        "RULE_NAME": {"type": "string"},
        "RULE_LHS": {
            "type": "array",
            "items":
                {
                    "type": "object",
                    "properties": {
                        "LHS_FACT_NAME": {"type": "string"},
                        "LHS_OP": {"type": "string"},
                        "LHS_VALUE": {"type": ["string", "number", "boolean"]}
                    },
                    "additionalProperties": False,
                    "minProperties": 3
                }
        },
        "RULE_RHS": {
            "type": "object",
            "properties": {
                "RHS_FACT_NAME": {"type": "string"},
                "RHS_FACT_VALUE": {"type": ["string", "number", "boolean"]}
            },
            "additionalProperties": False,
            "minProperties": 2
        },
        "COMMENT": {"type": ["string", "null"]},
        "ADD_DATE": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
    "minProperties": 5
}
