import sqlite3


DB_NAME = "Quiz_DB"
ANSWERS_TABLE_NAME = "answers"
QUESTIONS_TABLE_NAME = "questions"


# ANSWERS BLOCK
def create_answers_table(connection, cursor, table_name):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}"
                   "(user_id INTEGER,"
                   " user_name VARCHAR,"
                   " answer TEXT,"
                   " question TEXT)")
    connection.commit()


def add_answer(user_id, user_name, answer, question):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    create_answers_table(connection, cursor, ANSWERS_TABLE_NAME)

    cursor.execute(f"INSERT INTO {ANSWERS_TABLE_NAME} VALUES (?,?,?,?)",
                   (user_id, user_name, answer, question))
    connection.commit()


# QUESTIONS BLOCK
def create_questions_table(connection, cursor, table_name) -> None:
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}"
                   f"(question_text TEXT,"
                   f" responsed_users_id TEXT)")
    connection.commit()


def add_questions(questions_text_list: list) -> None:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    create_questions_table(connection, cursor, QUESTIONS_TABLE_NAME)

    cursor.executemany(f"INSERT INTO {QUESTIONS_TABLE_NAME} VALUES (?,?)", questions_text_list)
    connection.commit()


def get_questions() -> (bool, list):
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        return True, cursor.execute(f"SELECT question_text FROM {QUESTIONS_TABLE_NAME}").fetchall()
    except Exception:
        return False, []


def get_answered_users(question) -> list:
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        return [i for i in str(cursor.execute(
            f"SELECT responsed_users_id FROM {QUESTIONS_TABLE_NAME} WHERE question_text = ?",
            (question,)).fetchone()[0]).split(",") if i != ""]
    except Exception:
        return []


def users_to_string(users_list, new_user=None) -> str:
    return ",".join(users_list) + ("," if len(users_list) > 0 else "") + (f"{new_user}" if new_user is not None else "")


def append_responsed_users(user_id, question) -> bool:
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute(f"UPDATE {QUESTIONS_TABLE_NAME} SET responsed_users_id = ? WHERE question_text = ?",
                       (users_to_string(get_answered_users(question), user_id), question))
        connection.commit()
        return True
    except Exception:
        return False


# COMMON BLOCK
def drop_table(table_name) -> bool:
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute(f"DROP TABLE {table_name}")
        connection.commit()
        return True
    except Exception:
        return False
