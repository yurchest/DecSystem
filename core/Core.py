class Core:

    def __init__(self, db_session):
        self.db = db_session
        self.rules = self.__get_rules()
        self.rule_names = list(map(lambda x: x[0], self.db.get_rule_names()))

        print(self.rules)

    def __get_rules(self) -> dict:
        rules = {}
        for record in self.db.get_all_records("RULES_PARSED"):
            rule_name = record[0]

            if rule_name not in rules:
                rules[rule_name] = []

            rules[rule_name].append({
                "LHS_FACT_NAME": record[1],
                "LHS_OP": record[2],
                "LHS_VALUE": record[3],
                "RHS": record[4],
                "COMMENT": record[5],
            })
        return rules

    def add_fact(self):
        pass

    def check_condition(self) -> bool:
        pass

    def add_rule(self, rule: dict):
        pass
