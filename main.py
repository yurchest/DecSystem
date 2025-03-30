from database import db_Session
import core
import utils
import json
from catboost import CatBoostClassifier
import pandas as pd
import random
import joblib

feature_names = ['enc_loans_credit_status_3', 'enc_loans_credit_type_2', 'is_zero_util_0', 'enc_paym_16_0', 'enc_loans_credit_type_5', 'pre_util_16', 'pre_util_17', 'enc_paym_4_1', 'enc_paym_2_1', 'enc_paym_14_0', 'enc_loans_credit_status_5', 'pre_loans_outstanding_5', 'enc_paym_22_0', 'pre_loans_credit_cost_rate_11', 'enc_paym_23_0', 'enc_paym_20_1', 'enc_paym_13_0', 'enc_paym_1_1', 'pre_util_18', 'enc_paym_9_0', 'pre_since_opened_12', 'enc_paym_4_0', 'enc_paym_24_1', 'pre_loans_max_overdue_sum_1', 'enc_paym_18_0', 'enc_paym_5_0', 'enc_paym_1_0', 'enc_paym_19_0', 'enc_paym_3_0', 'is_zero_loans90_0', 'pre_loans_credit_limit_2', 'is_zero_loans6090_0', 'enc_paym_2_0', 'pre_loans_credit_cost_rate_6', 'enc_paym_0_1', 'pre_till_pclose_10', 'is_zero_loans3060_0', 'is_zero_loans530_0', 'enc_loans_credit_type_0', 'pre_util_6', 'pre_util_3']

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

def predict_pd(data: pd.DataFrame):
    model = CatBoostClassifier()
    model.load_model('model/model.cbm') 
    # model = joblib.load('model/calibrated_catboost.joblib')


    probabilities = model.predict_proba(data)  # возвращает вероятности классов
    print(f"Предсказание: {probabilities[0][1]}")
    return probabilities[0][1]

def get_feature_names():
    model = CatBoostClassifier()
    # model = joblib.load('model/model.joblib')
    # return model.estimator.feature_names_

    model.load_model('model/model.cbm') 
    return model.feature_names_   


def get_test_features():
    def get_random_row_from_pickle(file_path):
        # Сначала получаем общее количество строк
        df_len = len(pd.read_pickle(file_path))
        
        # Генерируем случайный индекс
        random_index = random.randint(0, df_len - 1)
        
        # Читаем только нужную строку
        return pd.read_pickle(file_path).iloc[[random_index]]

    df = get_random_row_from_pickle('model/data/data_all.pkl')
    print(f"target = {df['flag']}")
    df = df.filter(get_feature_names())
    return df



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

features = get_test_features()
predict_pd(features)