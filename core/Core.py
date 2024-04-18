import utils


class Core:

    def __init__(self, db_session):
        self.db = db_session
        self.facts_db = self.__get_facts_db()
        self.fact_names = list(self.facts_db.keys())
        self.rules = self.__get_rules()
        self.rule_names = list(self.rules.keys())

        self.facts = self.__init_facts()

        self.__validate_rules_with_facts()

    def __get_rules(self) -> dict:
        """
        Получение правил из БД
        :return: Словарь правил
        """
        rules = {}
        for record in self.db.get_all_records("RULES_PARSED"):
            rule_name = record[0]

            if rule_name not in rules:
                rules[rule_name] = []

            rules[rule_name].append({
                "LHS_FACT_NAME": record[1],
                "LHS_OP": record[2],
                "LHS_VALUE": utils.retype_fact_value(record[3], self.facts_db[record[1]]["FACT_TYPE"]),
                "RHS": record[4],
                "COMMENT": record[5],
            })
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
        for rule_name, rule in self.rules.items():
            print(rule_name, rule) # TODO
            pass

    def __validate_rules_with_facts(self) -> None:
        """
        Проверка наличия фактов, используемых в правилах, в БД фактов
        Проверка типов данных в правилах и БД фактах
        :return: None
        """

        # 1. Проверка наличия фактов, используемых в правилах, в БД фактов
        # Получение set всех фактов в правилах
        facts_in_rules = set()
        for rule in self.rules.values():
            for condition in rule:
                facts_in_rules.add(condition['LHS_FACT_NAME'])

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
        for rule_name, rules_list in self.rules.items():
            for rule in rules_list:
                fact_name = rule["LHS_FACT_NAME"]
                fact_value = rule["LHS_VALUE"]
                right_fact_type = self.facts_db[rule["LHS_FACT_NAME"]]["FACT_TYPE"]
                if not utils.is_fact_type(fact_value, right_fact_type):
                    print(f"В правиле {rule_name} факт {fact_name} не имеет тип {right_fact_type}")
                    exit(-1)

    def declare_fact(self, fact_name: str, fact_value) -> None:
        """
        Декларирование факта (добавление факта в рабочую память)
        :param fact_name:
        :param fact_value:
        :return: None
        """
        fact_value = utils.retype_fact_value(fact_value, self.facts_db[fact_name]["FACT_TYPE"])
        if self.__is_validated_fact_to_declare(fact_name, fact_value):
            self.facts[fact_name] = fact_value
        else:
            print(f"Факт не прошел валидацию")  # TODO

    def __is_validated_fact_to_declare(self, fact_name: str, fact_value) -> bool:
        """
        Проверка наличия факта в БД и проверка типа задаваемого факта
        :param fact_name:
        :param fact_value:
        :return: True / False
        """
        if fact_name not in self.fact_names:
            return False

        right_fact_type = self.facts_db[fact_name]["FACT_TYPE"]
        if utils.is_fact_type(fact_value, right_fact_type):
            return True
        else:
            return False

    def check_condition(self, rule: list) -> bool:
        pass

    def add_rule(self, rule: dict):
        pass
