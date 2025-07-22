import re
import sys
from datetime import datetime
from typing import Optional
from uuid import UUID

import pandas as pd
import psycopg2
from config.settings import settings
from helpers import load_json
from models.question_model import QuestionType


class InitialParser:
    @staticmethod
    def get_conn():
        try:
            conn = psycopg2.connect(**settings.DB_CREDS)
        except Exception as e:
            print("Unable to connect to the database:", e)
            sys.exit(1)

        return conn

    @staticmethod
    def clear_question_text(question_text):
        # regexp для текста вопроса
        #   1. ^\d+\.\s*     - matches the leading number, dot and any whitespace.
        #   2. (.+?)         - lazily captures the question text up until the first colon.
        #   3. :             - matches the colon after the text.
        #   4. (?:\s*- Строка \d+ -\s*(Оценка|Важность критерия))? - optionally matches the suffix specification.
        pattern = re.compile(r"^\d+\.\s*(.+?):" r"(?:\s*- Строка \d+ -\s*(Оценка|Важность критерия))?\s*$")

        match = pattern.match(question_text)
        if match:
            main_text = match.group(1).strip()
            # Если есть colon (or extra spaces then colon), убираем
            if main_text.endswith(":"):
                main_text = main_text[:-1].rstrip()
            suffix = match.group(2)  # Could be either "Оценка" or "Важность критерия" or None
            if suffix == "Важность критерия":
                main_text += f" ({suffix})"
        else:
            main_text = re.sub(r"^\d+\.\s*", "", question_text).strip()
            if main_text.endswith(":"):
                main_text = main_text[:-1].rstrip()

        return main_text

    def run(self):
        # read xlsx
        df = pd.read_excel("data/Расчет для презентации.xlsx", sheet_name="База", usecols="B:AP")  # noqa
        df = df[df["ИНН"].notna()]

        header = df.columns

        conn = self.get_conn()
        # create main survey
        main_survey_id = self.create_main_survey(conn)

        # create categories
        questions_map = load_json("questions_map.json")
        categories_map = {}
        for category_name, question_text in questions_map.items():
            category_id = self.insert_category(conn, category_name)
            categories_map[question_text] = category_id

        # create questions
        question_map = {}
        print(categories_map)
        for i, question_text in enumerate(header[4:], start=4):
            cleared = self.clear_question_text(question_text)
            category_id = categories_map.get(cleared, None)
            question_uid = self.insert_question(conn, main_survey_id, question_text, category_id)
            question_map[i] = question_uid

        for i, row in df.iterrows():
            # create client
            tin = int(row[0])
            preferences = row[1].strip()
            division = row[2].strip()
            ca_type = row[3].strip()
            client_id = self.insert_client(conn, tin, preferences, division, ca_type)
            if not client_id:
                print("Could not insert client for row:", row)
                continue

            # For each question column (starting at column index 4), insert answer
            for idx, answer in enumerate(row[4:], start=4):
                question_id = question_map[idx]
                if question_id is None:
                    continue

                self.insert_answer(conn, client_id, main_survey_id, question_id, answer)

        conn.close()
        print("Import complete.")

    @staticmethod
    def create_main_survey(conn):
        """
        Создание "main" опроса (from now to now + 30 days)
        """
        cur = conn.cursor()
        now = datetime.now()
        end_date = now.replace(day=now.day + 30) if now.day <= 1 else now

        insert_query = """
            INSERT INTO surveys (name, start_date, end_date)
            VALUES (%s, %s, %s)
            RETURNING uuid;
        """
        try:
            cur.execute(insert_query, ("Main Survey", now, end_date))
            survey_id = cur.fetchone()[0]
            conn.commit()
            print("Создан основной опроc ", survey_id)
            return survey_id
        except Exception as e:
            conn.rollback()
            print("Error creating main survey:", e)
            sys.exit(1)
        finally:
            cur.close()

    @staticmethod
    def insert_category(conn, category_name) -> Optional[UUID]:
        """
        Создание "main" опроса (from now to now + 30 days)
        """
        cur = conn.cursor()
        try:
            cur.execute(f"INSERT INTO categories (text) VALUES ('{str(category_name)}') RETURNING uuid;")
            category_id = cur.fetchone()[0]
            conn.commit()
            print("Создана категория ", category_name)
            return category_id
        except Exception as e:
            conn.rollback()
            print("Error creating category:", e)
            return None
        finally:
            cur.close()

    @classmethod
    def insert_question(cls, conn, survey_id, question_text, category_id) -> Optional[UUID]:
        """Добавляет запись в questions и возвращает id"""
        main_text = cls.clear_question_text(question_text)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO questions (survey_id, category_id, text, type) VALUES (%s, %s, %s, %s) RETURNING uuid;",
                (
                    str(survey_id),
                    str(category_id) if category_id else None,
                    main_text,
                    (
                        QuestionType.STRING.value
                        if main_text.startswith("В свободной форме")
                        or main_text.startswith("Пользовались ли Вы ранее сайтом")
                        else QuestionType.NUMERIC.value
                    ),
                ),
            )
            question_id = cur.fetchone()[0]
            conn.commit()
            return question_id
        except Exception as e:
            conn.rollback()
            print("Error inserting question", e)
            return None
        finally:
            cur.close()

    @staticmethod
    def insert_client(conn, tin, preferences, division, ca_type) -> Optional[UUID]:
        """Добавляет запись в таблицу clients и возвращает uuid"""
        cur = conn.cursor()
        insert_query = """
            INSERT INTO clients (tin, preferences, division, ca_type)
            VALUES (%s, %s, %s, %s)
            RETURNING uuid;
        """
        try:
            cur.execute(insert_query, (tin, preferences, division, ca_type))
            client_id = cur.fetchone()[0]
            conn.commit()
            return client_id
        except Exception as e:
            conn.rollback()
            print("Error inserting client", e)
            return None
        finally:
            cur.close()

    @staticmethod
    def insert_answer(conn, client_id, survey_id, question_id, ans_val):
        """Добавляет запись в таблицу answers"""
        cur = conn.cursor()

        # пытаемся перевести в int
        answer_int = None
        answer_text = None
        try:
            answer_int = int(ans_val)
        except Exception:
            answer_text = ans_val

        insert_query = """
            INSERT INTO answers (client_id, survey_id, question_id, answer_int, answer_text)
            VALUES (%s, %s, %s, %s, %s);
        """
        try:
            cur.execute(insert_query, (client_id, survey_id, question_id, answer_int, answer_text))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error inserting answer", e)
        finally:
            cur.close()


if __name__ == "__main__":
    parser = InitialParser()
    parser.run()
