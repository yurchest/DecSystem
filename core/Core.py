import utils


class Core:
    rules_activated = set()

    def __init__(self, db_session):
        self.db = db_session
        self.facts_db = self.__get_facts_db()
        self.fact_names = list(self.facts_db.keys())
        self.rules = self.__get_rules()

        self.facts = self.__init_facts()
        self.__validate_rules_with_facts()

    def __get_rules(self) -> list:
        """
        Получение правил из БД
        :return: Список правил
        """
        rules = list()
        for rule_record in self.db.get_all_records("RULES"):
            # print(rule_record)
            rule_name = rule_record[0]
            rule_rhs = {
                "RHS_FACT_NAME": rule_record[1],
                "RHS_FACT_VALUE": utils.retype_fact_value(rule_record[2], self.facts_db[rule_record[1]]["FACT_TYPE"])
            }
            rule_add_date = rule_record[3]
            rule_comment = rule_record[4]

            rule_lhs = []
            rule_lhs_record = self.db.select_many("""SELECT * from RULES_LHS WHERE RULE_NAME in (?)""", [rule_name])
            for lhs in rule_lhs_record:
                rule_lhs.append({
                    "LHS_FACT_NAME": lhs[1],
                    "LHS_OP": lhs[2],
                    "LHS_VALUE": utils.retype_fact_value(lhs[3], self.facts_db[lhs[1]]["FACT_TYPE"]),
                })

            rule = {
                "RULE_NAME": rule_name,
                "RULE_LHS": rule_lhs,
                "RULE_RHS": rule_rhs,
                "COMMENT": rule_comment,
                "ADD_DATE": rule_add_date,
            }
            rules.append(rule)

        return rules

    def __get_facts_db(self):
        """
        Получение информации о фактах из БД
        :return: Словарь фактов
        """
        records = self.db.get_facts()
        facts = dict((item['FACT_NAME'], item) for item in records)
        return facts

    def __init_facts(self) -> dict:
        """
        Инициализация словаря текущих фактов
        :return: Словарь фактов
        """
        facts = dict()
        for i in self.fact_names:
            facts[i] = None
        return facts

    def start(self):
        for rule in self.rules:
            rule_name = rule["RULE_NAME"]
            # rule_lhs_list = rule[1].split(";")
            rule_rhs_fact_name = rule["RULE_RHS"]["RHS_FACT_NAME"]
            rule_rhs_fact_value = rule["RULE_RHS"]["RHS_FACT_VALUE"]
            rule_rhs_fact_value = utils.retype_fact_value(rule_rhs_fact_value, self.facts_db[rule_rhs_fact_name]["FACT_TYPE"])
            if self.__is_true_rule(rule["RULE_LHS"]):
                if self.facts[rule_rhs_fact_name] != rule_rhs_fact_value:
                    print(f"Сработало правило {rule_name}")
                    self.rules_activated.add(rule_name)
                    self.declare_fact(rule_rhs_fact_name, rule_rhs_fact_value)
                    print(self.facts)
                    self.start()

    def __validate_rules_with_facts(self) -> None:
        """
        Проверка наличия фактов, используемых в правилах, в БД фактов
        Проверка типов данных в правилах и БД фактах
        :return: None
        """

        # 1. Проверка наличия фактов, используемых в правилах, в БД фактов
        # Получение set всех фактов в правилах
        facts_in_rules = set()
        for rule in self.rules:
            for lhs in rule["RULE_LHS"]:
                facts_in_rules.add(lhs['LHS_FACT_NAME'])

            facts_in_rules.add(rule["RULE_RHS"]["RHS_FACT_NAME"])

        facts_in_facts_db = set(self.fact_names)

        # Если множество фактов из правил в множестве фактов из БД
        if facts_in_rules.issubset(facts_in_facts_db):
            pass  # TODO
        else:
            # элементы первого списка которые НЕ находятся во втором списке
            minus_sets = facts_in_rules - facts_in_facts_db
            print(f"Факты {minus_sets} не инициализированы")
            exit(-1)  # TODO

        # 2. Проверка типов данных в правилах и БД фактах
        for rule in self.rules:
            for lhs in rule["RULE_LHS"]:
                fact_name = lhs["LHS_FACT_NAME"]
                fact_value = lhs["LHS_VALUE"]
                right_fact_type = self.facts_db[fact_name]["FACT_TYPE"]
                if not utils.is_fact_type(fact_value, right_fact_type):
                    print(f"В правиле {rule['RULE_NAME']} факт {fact_name} не имеет тип {right_fact_type}")
                    exit(-1)

    def declare_fact(self, fact_name: str, fact_value) -> None:
        """
        Декларирование факта (добавление факта в рабочую память)
        :param fact_name:
        :param fact_value:
        :return: None
        """
        # Проверка наличия факта в БД
        if fact_name not in self.fact_names:
            print(f"Факт '{fact_name}' не прошел валидацию")  # TODO
            return
        fact_value = utils.retype_fact_value(fact_value, self.facts_db[fact_name]["FACT_TYPE"])
        if self.__is_validated_fact_to_declare(fact_name, fact_value):
            self.facts[fact_name] = fact_value
        else:
            print(f"Факт '{fact_name}' не прошел валидацию")  # TODO
            return

    def __is_validated_fact_to_declare(self, fact_name: str, fact_value) -> bool:
        """
        Проверка типа задаваемого факта
        :param fact_name:
        :param fact_value:
        :return: True / False
        """

        right_fact_type = self.facts_db[fact_name]["FACT_TYPE"]
        if utils.is_fact_type(fact_value, right_fact_type):
            return True
        else:
            return False

    def __is_true_rule(self, rules: list) -> bool:
        fl_list = []
        for rule in rules:
            fact_name = rule["LHS_FACT_NAME"]
            op = rule["LHS_OP"]
            value = rule["LHS_VALUE"]
            current_fact_value = self.facts[fact_name]
            fl_list.append(utils.get_truth(current_fact_value, op, value))

        return True if all(fl_list) else False

    def add_rule(self, rule: dict):
        pass
