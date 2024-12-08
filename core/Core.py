import utils
from operator import itemgetter


class Core:
    rules_activated = set()

    def __init__(self, db_session):
        self.db = db_session
        self.facts_db = self.__get_facts_db()
        self.fact_names = list(self.facts_db.keys())
        self.rules = self.__get_rules()
        self.rule_names = self.__get_rule_names()
        self.facts = self.__init_facts()
        self.validate_rules_with_facts()

        print(self.facts)
        print(*self.rules, sep="\n")

    def __get_rules(self) -> list:
        """
        Получение правил из БД
        :return: Список правил
        """
        rules = list()
        for rule_record in sorted(self.db.get_all_records("RULES"), key=itemgetter(5)):
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

    def __get_rule_names(self):
        rule_names = self.db.select_many("""SELECT RULE_NAME from RULES""")
        return [x[0] for x in rule_names]

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
            facts[i] = self.facts_db[i]["DEFAULT_VALUE"]
        return facts

    def start(self):
        for rule in self.rules:
            rule_name = rule["RULE_NAME"]
            # rule_lhs_list = rule[1].split(";")
            rule_rhs_fact_name = rule["RULE_RHS"]["RHS_FACT_NAME"]
            rule_rhs_fact_value = rule["RULE_RHS"]["RHS_FACT_VALUE"]
            rule_rhs_fact_value = utils.retype_fact_value(rule_rhs_fact_value,
                                                          self.facts_db[rule_rhs_fact_name]["FACT_TYPE"])
            if self.__is_true_rule(rule["RULE_LHS"]):
                if self.facts[rule_rhs_fact_name] != rule_rhs_fact_value \
                        and self.facts[rule_rhs_fact_name] == self.facts_db[rule_rhs_fact_name]["DEFAULT_VALUE"]:
                    # Для предотвращения бесконечной рекурсии (зацикливания) факт можно обновлять только один раз

                    # print(f"Сработало правило {rule_name}")
                    self.rules_activated.add(rule_name)
                    self.declare_fact(rule_rhs_fact_name, rule_rhs_fact_value)
                    # print(self.facts)
                    self.start()

    def __validate_rule_with_facts(self, rule: dict) -> dict:
        error_messages = []
        # 1. Проверка наличия фактов, используемых в правиле, в БД фактов
        # Получение set всех фактов в правилах
        fact_in_rules = set()
        for lhs in rule["RULE_LHS"]:
            fact_in_rules.add(lhs['LHS_FACT_NAME'])

        fact_in_rules.add(rule["RULE_RHS"]["RHS_FACT_NAME"])

        facts_in_facts_db = set(self.fact_names)

        # Если множество фактов из правил в множестве фактов из БД
        if fact_in_rules.issubset(facts_in_facts_db):
            pass  # TODO
        else:
            # элементы первого списка которые НЕ находятся во втором списке
            minus_sets = fact_in_rules - facts_in_facts_db
            error_messages.append(
                f"Ошибка валидации правила {rule['RULE_NAME']}.Факт(ы) {minus_sets} не инициализированы")

        # 2. Проверка типов данных в правилах и БД фактах
        for lhs in rule["RULE_LHS"]:
            fact_name = lhs["LHS_FACT_NAME"]
            fact_value = utils.retype_fact_value(lhs["LHS_VALUE"], self.facts_db[fact_name]["FACT_TYPE"])
            right_fact_type = self.facts_db[fact_name]["FACT_TYPE"]
            if not utils.is_fact_type(fact_value, right_fact_type):
                error_messages.append(
                    f"Ошибка валидации правила {rule['RULE_NAME']}. В правиле {rule['RULE_NAME']} факт \
                        {fact_name} не имеет тип {right_fact_type}")

        if not error_messages:
            return utils.return_message("success", None)
        else:
            return utils.return_message("error", error_messages)

    def validate_rules_with_facts(self) -> dict:
        """
        Проверка наличия фактов, используемых в правилах, в БД фактов
        Проверка типов данных в правилах и БД фактах
        :return: list[dict]
        """
        error_messages = []
        for rule in self.rules:
            validation_result = self.__validate_rule_with_facts(rule)
            if validation_result["messages"] is not None:
                error_messages.extend(validation_result["messages"])
        if not error_messages:
            return utils.return_message("success", None)
        else:
            return utils.return_message("error", error_messages)

    def declare_fact(self, fact_name, fact_value):
        self.facts[fact_name] = fact_value

    def declare_multiply_facts(self, facts: dict):
        error_messages = []
        for fact_name, fact_value in facts.items():
            validation_result = self.__validate_fact_to_declare(fact_name, fact_value)
            if validation_result["messages"] is not None:
                error_messages.extend(validation_result["messages"])

        if not error_messages:
            for fact_name, fact_value in facts.items():
                self.facts[fact_name] = utils.retype_fact_value(fact_value, self.facts_db[fact_name]["FACT_TYPE"])
            return utils.return_message("success", None)
        else:
            return utils.return_message("error", error_messages)

    def __validate_fact_to_declare(self, fact_name, fact_value) -> dict:
        error_messages = []
        # Проверка наличия факта в БД
        if fact_name not in self.fact_names:
            error_messages.append(f"Факт '{fact_name}' не инициализирован")
        fact_value = utils.retype_fact_value(fact_value, self.facts_db[fact_name]["FACT_TYPE"])
        if not self.__is_declared_type_is_right_type(fact_name, fact_value):
            error_messages.append(f"Факт '{fact_name}' имеет неинициализированный тип")

        if not error_messages:
            return utils.return_message("success", None)
        else:
            return utils.return_message("error", error_messages)

    def __is_declared_type_is_right_type(self, fact_name: str, fact_value) -> bool:
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
            # print(current_fact_value, op, value)
            fl_list.append(utils.get_truth(current_fact_value, op, value))
        return True if all(fl_list) else False

    def add_fact(self, fact: dict) -> dict:
        """
        Добавление факта в список используемых фактов в БД
        :param fact:
        :return:
        """
        validation_result = self.__validate_fact_to_add(fact)
        if validation_result["status"] == "success":
            self.db.add_fact(fact)
            return utils.return_message("success", None)
        else:
            return utils.return_message("error", validation_result["messages"])

    def __validate_fact_to_add(self, fact: dict):
        if not utils.is_validated_schema(fact, utils.init_fact_schema):
            return utils.return_message("error", [f"Факт не прошел валидацию по схеме и не был добавлен"])
        if fact["FACT_NAME"] in self.fact_names:
            return utils.return_message("error", [f"Факт уже существует"])

        return utils.return_message("success", None)

    def add_rule(self, rule: dict) -> dict:
        """
        Добавление правила в систему
        Логика:
        1. Валидация правила
        2. Добавление в БД
        3. Обновление self.rules путем запроса к БД
        :param rule:
        :return:
        """
        validation_result = self.__validate_rule_to_add(rule)
        if validation_result["status"] == "success":
            self.db.add_rule(rule)
            return validation_result
        else:
            return validation_result

    def __validate_rule_to_add(self, rule: dict) -> dict:
        if not utils.is_validated_schema(rule, utils.ruleSchema):
            return utils.return_message("error", ["Правило не прошло валидацию по схеме"])
        # Рул уже существует
        if rule["RULE_NAME"] in self.rule_names:
            return utils.return_message("error", [f"Правило с именем '{rule['RULE_NAME']}' уже существует"])
        validation_result = self.__validate_rule_with_facts(rule)
        if validation_result["status"] != "success":
            return validation_result

        # Поиск возможности объединения / пересечения правил
        res = self.get_similar_rules(rule)
        if res["status"] != "success":
            return utils.return_message("success", [f"Найдены похожие правила {res['messages']}"])
        return utils.return_message("success", None)

    def get_similar_rules(self, rule_to_add) -> dict:
        # lhs_fact_name_to_add
        similar_rules = []
        for rule in self.rules:
            if rule["RULE_RHS"]["RHS_FACT_NAME"] == rule_to_add["RULE_RHS"]["RHS_FACT_NAME"] \
                    and rule["RULE_RHS"]["RHS_FACT_VALUE"] == rule_to_add["RULE_RHS"]["RHS_FACT_VALUE"] \
                    and set([x["LHS_FACT_NAME"] for x in rule["RULE_LHS"]]) == \
                    set([x["LHS_FACT_NAME"] for x in rule_to_add["RULE_LHS"]]):

                similar_rules.append(rule["RULE_NAME"])
        if similar_rules is None:
            return utils.return_message("success", None)
        else:
            return utils.return_message("warning", similar_rules)
