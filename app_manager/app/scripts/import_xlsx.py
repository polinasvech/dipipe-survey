import re
import sys
from datetime import datetime

import pandas as pd
import psycopg2
from config.settings import settings


class InitialParser:
    @staticmethod
    def get_conn():
        try:
            conn = psycopg2.connect(**settings.DB_CREDS)
        except Exception as e:
            print("Unable to connect to the database:", e)
            sys.exit(1)

        return conn

    def run(self):
        # read xlsx
        df = pd.read_excel("data/Расчет для презентации.xlsx", sheet_name="База", usecols="B:AP")  # noqa
        df = df[df["ИНН"].notna()]

        header = df.columns

        conn = self.get_conn()
        # create main survey
        main_survey_id = self.create_main_survey(conn)

        # create questions
        question_map = {}
        for i, question_text in enumerate(header[4:], start=4):
            print(i, question_text)
            question_uid = self.insert_question(conn, main_survey_id, question_text)
            question_map[i] = question_uid

        for i, row in df.iterrows():
            # Insert client record.
            tin = int(row[0])
            preferences = row[1].strip()
            division = row[2].strip()
            ca_type = row[3].strip()
            client_id = self.insert_client(conn, tin, preferences, division, ca_type)
            print("CHECKCLIENT", client_id)
            if not client_id:
                print("Could not insert client for row:", row)
                continue

            # For each question column (starting at column index 4), insert answer.
            for idx, answer in enumerate(row[4:], start=4):
                question_id = question_map[idx]
                if question_id is None:
                    # Skip if no valid question record was created.
                    continue

                # Insert answer record.
                self.insert_answer(
                    conn, client_id, main_survey_id, question_id, answer
                )

        conn.close()
        print("Import complete.")

    @staticmethod
    def create_main_survey(conn):
        """
        Создание "main" опроса (from now to now + 30 days)
        """
        cur = conn.cursor()
        now = datetime.now()
        # end_date: 30 days later
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
    def insert_question(conn, survey_id, question_text):
        """Добавляет запись в questions и возвращает id"""
        # regexp для текста вопроса
        pattern = re.compile(
            r"^(?:\d+\.\s*)(.*?)(?:\s*-\s*Строка\s+\d+\s*-\s*.+)?\s*$", re.UNICODE
        )
        cleared_text = pattern.match(question_text)
        if not cleared_text:
            return

        cur = conn.cursor()
        insert_query = """
            INSERT INTO questions (survey_id, text)
            VALUES (%s, %s)
            RETURNING uuid;
        """
        try:
            cur.execute(insert_query, (survey_id, cleared_text.group(1)))
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
    def insert_client(conn, tin, preferences, division, ca_type):
        """
        Insert a record into clients table.
        Assumes the table definition:
          clients(uuid, tin, preferences, division, ca_type)
        """
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
        """
        Insert a record into answers table.
        If ans_val can be interpreted as an integer, store it in answer_int;
        otherwise store it as answer_text.
        NOTE: The table's primary key should ideally include question_id
              because one client can answer more than one question.
        """
        cur = conn.cursor()
        # Try converting the answer to an integer.
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
            cur.execute(
                insert_query, (client_id, survey_id, question_id, answer_int, answer_text)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error inserting answer", e)
        finally:
            cur.close()


if __name__ == "__main__":
    parser = InitialParser()
    parser.run()
