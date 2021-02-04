import database_common
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT id, image, message, submission_time, vote_number
        FROM answer
        WHERE question_id={}
        ORDER BY id""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_by_question(cursor: RealDictCursor, question_id:int) -> list:
    query = """
    SELECT id, name
    FROM tag
    JOIN question_tag 
    ON tag.id = question_tag.tag_id
    WHERE question_id = {}""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def remove_tags_from_question(cursor: RealDictCursor, question_id:int) -> list:
    query = """
    DELETE
    FROM question_tag
    WHERE question_id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def remove_tag(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = """
    DELETE FROM question_tag
    WHERE question_id = {} AND tag_id = {}""".format(question_id, tag_id)
    cursor.execute(query)


@database_common.connection_handler
def write_answer(cursor: RealDictCursor, question_id: int, modifications: dict) -> list:
    if modifications['image'] is not None:
        query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}', '{}');"""\
            .format(question_id, modifications['message'], modifications['image'])
        cursor.execute(query)
    else:
        query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}');""".format(question_id, modifications['message'])
        cursor.execute(query)


@database_common.connection_handler
def modify_answer(cursor: RealDictCursor, answer_id: int, modifications: dict) -> list:
    query = """
    UPDATE answer
    SET message= '{}'
    WHERE id = {};""".format(modifications['message'], answer_id)
    cursor.execute(query)
    if modifications['image'] is not None:
        query = """
            UPDATE answer
            SET image = '{}'
            WHERE id = {};""".format(modifications['image'], answer_id)
        cursor.execute(query)

@database_common.connection_handler
def write_comment(cursor: RealDictCursor, question_id: int, comment: str) -> list:
    query = """
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
    VALUES ({}, NULL ,'{}',CURRENT_TIMESTAMP,0);""".format(question_id, comment)
    cursor.execute(query)

@database_common.connection_handler
def write_answer_comment(cursor: RealDictCursor, question_id: int, answer_id: int, comment: str) -> list:
    query = """
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
    VALUES ({}, {} ,'{}',CURRENT_TIMESTAMP,0);""".format(question_id, answer_id, comment)
    cursor.execute(query)

@database_common.connection_handler
def get_comment(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    SELECT question_id, answer_id, message, submission_time
    FROM comment
    WHERE question_id = {};""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = {}""".format(answer_id)
    cursor.execute(query)


@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = {}""".format(answer_id)
    cursor.execute(query)


@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = {}""".format(question_id)
    cursor.execute(query)


@database_common.connection_handler
def get_answer_data(cursor: RealDictCursor, answer_id: int) -> tuple:
    query = """
        SELECT question_id, message, image
        FROM answer
        WHERE id = {}""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def search(cursor: RealDictCursor, word: str) -> list:
    query = """
        SELECT DISTINCT title, q.message, q.submission_time, view_number, q.vote_number
        FROM question AS q LEFT JOIN answer AS a
        ON q.id = a.question_id
        WHERE UPPER(title) LIKE UPPER('%%{}%%') OR UPPER(q.message) LIKE UPPER('%%{}%%')
        ORDER BY submission_time DESC;""".format(word, word, word)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_answers(cursor: RealDictCursor, word: str) -> list:
    query = """
        SELECT DISTINCT title, q.message, q.submission_time, view_number, q.vote_number, a.message AS answer_message
        FROM question AS q LEFT JOIN answer AS a
        ON q.id = a.question_id
        WHERE a.message LIKE '%%{}%%'
        ORDER BY submission_time DESC;""".format(word, word, word)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    DELETE FROM answer
    WHERE id = {}""".format(answer_id)
    cursor.execute(query)


@database_common.connection_handler
def get_question_answers(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    SELECT id FROM answer
    WHERE question_id = {}""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    DELETE FROM question
    WHERE id = {};
    DELETE FROM answer
    WHERE question_id = {}""".format(question_id, question_id)
    cursor.execute(query)


@database_common.connection_handler
def get_latest_five_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time 
        DESC LIMIT 5;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * 
        FROM question
        WHERE id = {};""".format(question_id)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_questions_sorted(cursor: RealDictCursor, parameter: str, direction: str ) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY {} {};""".format(parameter, direction)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor: RealDictCursor, question: dict) -> list:
    if question['image'] is not None:
        query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES(CURRENT_TIMESTAMP, 0, 0, '{}', '{}', '{}') RETURNING id;""" \
            .format(question["title"], question['message'], question['image'])
        cursor.execute(query)
    else:
        query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message)
        VALUES(CURRENT_TIMESTAMP, 0, 0, '{}', '{}') RETURNING id;""" \
            .format(question["title"], question['message'])
        cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def modify_question(cursor: RealDictCursor, question_id: int, modifications: dict) -> list:
    query = """
    UPDATE question
    SET title = '{}', message= '{}'
    WHERE id = {};""".format(modifications["title"], modifications['message'], question_id)
    cursor.execute(query)
    if modifications['image'] is not None:
        query = """
            UPDATE question
            SET image = '{}'
            WHERE id = {};""".format(modifications['image'], question_id)
        cursor.execute(query)


@database_common.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def save_tag(cursor: RealDictCursor, tag:str) -> list:
    query = """
    INSERT INTO
    tag (name)
    VALUES('{}')
    RETURNING *""".format(tag)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def add_tag_to_question(cursor: RealDictCursor,tag_id:int,question_id:int) -> list:
    query = """
    INSERT INTO
    question_tag (question_id, tag_id)
    VALUES({}, {})""".format(question_id, tag_id)
    cursor.execute(query)


@database_common.connection_handler
def delete_answers_by_question_id(cursor: RealDictCursor, question_id:int) -> list:
    query = """
    DELETE FROM answer
    WHERE question_id = {}""".format(question_id)
    cursor.execute(query)