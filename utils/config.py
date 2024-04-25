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
                        "LHS_VALUE": {"type": ["string", "number"]}
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
    },
    "additionalProperties": False,
    "minProperties": 4
}

fact_schema = {
    "type": "object",
    "properties": {
        "FACT_NAME": {"type": "string"},
        "FACT_TYPE": {"type": "string", "enum": ["text", "number", "bool"]},
        "COMMENT": {"type": "string"},
        "DEFAULT_VALUE": {"type": "string"}
    },
    "additionalProperties": False,
    "minProperties": 3
}
