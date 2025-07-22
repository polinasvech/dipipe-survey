import sys
from typing import Dict, Tuple
from uuid import UUID

import pandas as pd
import psycopg2
from config.settings import settings
from helpers import load_json


class Calculator:
    def __init__(self, survey_id: UUID):
        self.survey_id = survey_id

        self.metrics_map = load_json("metrics_map.json")
        self.questions_map = load_json("questions_map.json")

        self.main_df = self.prep_df()

    @staticmethod
    def get_conn():
        try:
            conn = psycopg2.connect(**settings.DB_CREDS)
        except Exception as e:
            print("Unable to connect to the database:", e)
            sys.exit(1)
        return conn

    def get_answers(self, question_text) -> pd.DataFrame:
        conn = self.get_conn()
        cur = conn.cursor()

        try:
            query = f"""
                select distinct on (clients.uuid, questions.text)
                  clients.uuid as client,
                  answer_int
                from answers
                join clients on clients.uuid = answers.client_id
                join questions on questions.uuid = answers.question_id
                where questions.survey_id = '{str(self.survey_id)}'
                and questions.text = '{question_text}'
                order by clients.uuid, questions.text, questions.uuid;
            """
            cur.execute(query)
            answers = cur.fetchall()
            df = pd.DataFrame(answers, columns=["client_id", question_text])
            df.fillna(0, inplace=True)
            return df

        except Exception as e:
            print("Error when fetching answers:", e)
            sys.exit(1)
        finally:
            cur.close()

    def calculate_nps(self) -> Tuple[Dict, float]:
        df = self.main_df.copy(deep=True)

        result = {category: dict() for category in self.questions_map}

        for category, q_text in self.questions_map.items():
            non_zero_answers = [i for i in df[q_text] if i != 0]
            result[category]["average"] = sum(non_zero_answers) / len(non_zero_answers)
            result[category]["promoters"] = sum(1 for i in non_zero_answers if i >= 9)
            result[category]["neutral"] = sum(1 for i in non_zero_answers if i in [7, 8])
            result[category]["critics"] = sum(1 for i in non_zero_answers if i <= 6)
            result[category]["promoters_percent"] = round(result[category]["promoters"] / len(non_zero_answers), 2)
            result[category]["neutral_percent"] = round(result[category]["promoters"] / len(non_zero_answers), 2)
            result[category]["critics_percent"] = round(result[category]["critics"] / len(non_zero_answers), 2)
            result[category]["nps_val"] = round(
                result[category]["promoters_percent"] - result[category]["critics_percent"], 2
            )

        avg_total = sum(val["average"] for val in result.values()) / len(result)

        return result, avg_total

    def calculate_correlations(self) -> Dict:
        ranks_df = self.main_df.copy(deep=True)
        ranks_df = ranks_df.drop("client_id", axis=1)
        for col in ranks_df.columns:  # для всех колонок кроме client_id вычисляем ранк
            ranks_df[col] = ranks_df[col].rank(method="average")

        main_metrics = {key: dict() for key in self.questions_map}
        for key, question_text in self.questions_map.items():
            for metric, q_text in self.metrics_map.items():
                main_metrics[key][metric] = round(ranks_df[q_text].corr(ranks_df[question_text], method="spearman"), 2)

        return main_metrics

    def get_main_metrics(self):
        """Подготавливает данные для круговых диаграмм для 'Лояльность', 'Удовлетворенность', 'Вероятность Повт. Покупки'"""
        df = self.main_df.copy(deep=True)
        questions_map = {
            "Какова вероятность, что Вы порекомендуете компанию как поставщика трубной продукции своим коллегам и партнерам?": "loyalty",
            "Оцените, пожалуйста, насколько вы удовлетворены взаимодействием с ТД ТМК": "satisfaction",
            "Какова вероятность, что при возникновении потребности в будущем вы выберете поставщиком ТД ТМК": "repeat_purchase",
        }
        df = df[questions_map.keys()]
        df.rename(columns=questions_map, inplace=True)

        total_respondents = len(df)  # общее кол-во ответивших
        stats = {}

        # Define ranges: critics (0-6), neutrals (7-8), promoters (9-10)
        for column in df.columns:
            critics = df[(df[column] >= 0) & (df[column] <= 6)][column].count()
            neutrals = df[(df[column] >= 7) & (df[column] <= 8)][column].count()
            promoters = df[(df[column] >= 9) & (df[column] <= 10)][column].count()

            stats[column] = {
                "Критики": round(critics / total_respondents * 100, 2),
                "Нейтралы": round(neutrals / total_respondents * 100, 2),
                "Сторонники": round(promoters / total_respondents * 100, 2),
            }

        return stats

    def prep_df(self) -> pd.DataFrame:
        """Собирает данные для анализа в общий df"""
        dataframes = []

        for metric, question_text in self.metrics_map.items():
            partial_df = self.get_answers(question_text)
            if not partial_df.empty:
                dataframes.append(partial_df)

        for metric, question_text in self.questions_map.items():
            partial_df = self.get_answers(question_text)
            if not partial_df.empty:
                partial_df.drop_duplicates(inplace=True, subset=["client_id"])
                dataframes.append(partial_df)

        result_df = dataframes[0]
        for frame in dataframes[1:]:
            result_df = pd.merge(result_df, frame, on="client_id", how="inner")

        return result_df
