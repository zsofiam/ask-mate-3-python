import database_common
import bcrypt
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# (try@feature.com - try)
# (admin@admin.com - admin)


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def get_user_data(cursor: RealDictCursor, username: str):
    query = """
    SELECT id, password
    FROM users
    WHERE username = '{}';""".format(username)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT id, image, message, submission_time, vote_number, accepted
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
        UPDATE users_statistics
        SET answer_count  = answer_count + 1
        WHERE user_id = {};
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}', '{}', {});"""\
            .format(modifications['user_id'], question_id, modifications['message'], modifications['image'], modifications['user_id'])
        cursor.execute(query)
    else:
        query = """
        UPDATE users_statistics
        SET answer_count  = answer_count + 1
        WHERE user_id = {};
        INSERT INTO answer (submission_time, vote_number, question_id, message, user_id)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}', {});"""\
            .format(modifications['user_id'], question_id, modifications['message'], modifications['user_id'])
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
def write_comment(cursor: RealDictCursor, question_id: int, comment: str, user_id: int):
    query = """
    UPDATE users_statistics
    SET comment_count = comment_count + 1
    WHERE user_id = {};
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
    VALUES ({}, NULL ,'{}',CURRENT_TIMESTAMP,0, {});""".format(user_id, question_id, comment, user_id)
    cursor.execute(query)


@database_common.connection_handler
def update_comment(cursor: RealDictCursor, id: int, comment: dict):
    query = """
    UPDATE comment
    SET message = '{}', edited_count = edited_count + 1
    WHERE id = {};""".format(comment["comment"], id)
    cursor.execute(query)


@database_common.connection_handler
def write_answer_comment(cursor: RealDictCursor, question_id: int, answer_id: int, comment: str, user_id: int):
    query = """
    UPDATE users_statistics
    SET comment_count = comment_count + 1
    WHERE user_id = {};
    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
    VALUES ({}, {} ,'{}',CURRENT_TIMESTAMP,0, {});""".format(user_id, question_id, answer_id, comment, user_id)
    cursor.execute(query)


@database_common.connection_handler
def get_comment(cursor: RealDictCursor, question_id: int) -> list:
    query = """
    SELECT id, question_id, answer_id, message, submission_time, edited_count
    FROM comment
    WHERE question_id = {};""".format(question_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_message_by_id(cursor: RealDictCursor, id: int) -> list:
    query = """
    SELECT message, question_id, id
    FROM comment
    WHERE id = {};""".format(id)
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_comment_id_by_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
    SELECT id
    FROM comment
    WHERE answer_id = {};""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment_by_id(cursor: RealDictCursor, comment_id: int, user_id: int):
    query = """
    UPDATE users_statistics
    SET comment_count = comment_count - 1
    WHERE user_id = {};
    DELETE FROM comment
    WHERE id = {}""".format(user_id, comment_id)
    cursor.execute(query)


@database_common.connection_handler
def delete_comments_by_question_id(cursor: RealDictCursor, question_id: int, user_id: int):
    query = """
    UPDATE users_statistics
    SET comment_count = comment_count - 1
    WHERE user_id = {};
    DELETE FROM comment
    WHERE question_id = {}""".format(user_id, question_id)
    cursor.execute(query)


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
        FROM question AS q FULL JOIN answer AS a
        ON q.id = a.question_id
        WHERE UPPER(a.message) LIKE UPPER('%%{}%%')
        ORDER BY submission_time DESC;""".format(word, word, word)
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id: int, user_id: int) -> list:
    query = """
    UPDATE users_statistics
    SET answer_count = answer_count - 1 
    WHERE user_id = {};
    DELETE FROM answer
    WHERE id = {}""".format(user_id, answer_id)
    cursor.execute(query)


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int, user_id: int) -> list:
    query = """
    UPDATE users_statistics
    SET question_count  = question_count - 1
    WHERE user_id = {};
    DELETE FROM question
    WHERE id = {};
    DELETE FROM answer
    WHERE question_id = {}""".format(user_id, question_id, question_id)
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
        UPDATE users_statistics
        SET question_count  = question_count + 1
        WHERE user_id = {};
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES(CURRENT_TIMESTAMP, 0, 0, '{}', '{}', '{}', {}) RETURNING id;""" \
            .format(question['user_id'], question["title"], question['message'], question['image'], question['user_id'])
        cursor.execute(query)
    else:
        query = """
        UPDATE users_statistics
        SET question_count  = question_count + 1
        WHERE user_id = {};
        INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id)
        VALUES(CURRENT_TIMESTAMP, 0, 0, '{}', '{}', {}) RETURNING id;""" \
            .format(question['user_id'], question["title"], question['message'], question['user_id'])
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
def delete_answers_by_question_id(cursor: RealDictCursor, question_id:int, user_id) -> list:
    query = """
    UPDATE users_statistics
    SET answer_count  = answer_count - 1
    WHERE user_id = {};
    DELETE FROM answer
    WHERE question_id = {}""".format(user_id, question_id)
    cursor.execute(query)


@database_common.connection_handler
def add_user(cursor: RealDictCursor, email:str,password:str):
    query = """
    INSERT INTO users(id,username,password,registration_date,reputation) 
    VALUES (DEFAULT,%s,%s,CURRENT_TIMESTAMP,0);"""
    cursor.execute(query, (email,password,))


@database_common.connection_handler
def get_user_id(cursor: RealDictCursor, email:str) -> list:
    query = """
    SELECT id
    FROM users
    WHERE username = (%s);"""
    cursor.execute(query, (email,))
    return cursor.fetchone()


@database_common.connection_handler
def get_users(cursor: RealDictCursor) -> list:
    query = """SELECT u.id, u.username, u.registration_date, u.reputation, 
    s.question_count, s.answer_count, s.comment_count FROM users u
    JOIN users_statistics s
    ON u.id = s.user_id"""
    cursor.execute(query)
    return cursor.fetchall()

# @database_common.connection_handler
# def get_users(cursor: RealDictCursor) -> list:
#     query = """SELECT u.id, u.username,
#      u.registration_date,
#      u.reputation,
#        count(q.id) as question_count,
#        count(a.id) as answer_count,
#        count(c.id) as comment_count
#         FROM users u
#         left JOIN question q on u.id = q.user_id
#         left JOIN comment c on u.id = c.user_id
#         left JOIN answer a on u.id = a.user_id
#         group by u.id, u.username, u.registration_date, u.reputation;
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


@database_common.connection_handler
def question_reputation_up(cursor: RealDictCursor, question_id:int):
    query = """ UPDATE users
	SET reputation = reputation + 5 
	WHERE id in (SELECT user_id FROM question WHERE id = (%s)); """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def question_reputation_down(cursor: RealDictCursor, question_id:int):
    query = """ UPDATE users
	SET reputation = reputation - 2 
	WHERE id in (SELECT user_id FROM question WHERE id = (%s)); """
    cursor.execute(query, (question_id,))


@database_common.connection_handler
def answer_reputation_up(cursor: RealDictCursor, answer_id: int):
    query = """ UPDATE users
    SET reputation = reputation + 10
    WHERE id in (SELECT user_id FROM answer WHERE id = (%s)); """
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def answer_reputation_down(cursor: RealDictCursor, answer_id: int):
    query = """ UPDATE users
    SET reputation = reputation - 2
    WHERE id in (SELECT user_id FROM answer WHERE id = (%s)); """
    cursor.execute(query, (answer_id,))

    
@database_common.connection_handler
def question_get_user_id(cursor: RealDictCursor, question_id: int):
    query = """select user_id
    from question
    where id = (%s);"""
    cursor.execute(query, (question_id,))
    return cursor.fetchone()

    
@database_common.connection_handler
def get_user_by_id(cursor: RealDictCursor, user_id: int):
    query = """SELECT u.id, u.username, u.registration_date, u.reputation, 
    s.question_count, s.answer_count, s.comment_count FROM users u
    JOIN users_statistics s
    ON u.id = s.user_id
    WHERE u.id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchone()


@database_common.connection_handler
def accept_answer(cursor: RealDictCursor, answer_id: int):
    query = """update answer
    set accepted = TRUE 
    where id = (%s);"""
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def unaccept_answer(cursor: RealDictCursor, answer_id: int):
    query = """update answer
    set accepted = FALSE 
    where id = (%s);"""
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def get_user_questions(cursor: RealDictCursor, user_id: int) -> list:
    query = """SELECT * FROM question
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_user_answers(cursor: RealDictCursor, user_id: int) -> list:
    query = """SELECT * FROM answer
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_user_comments(cursor: RealDictCursor, user_id: int) -> list:
    query = """SELECT * FROM comment
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@database_common.connection_handler
def get_tags(cursor: RealDictCursor) ->list:
    query = """ SELECT COUNT(question_tag.tag_id) , tag.name
	FROM question_tag
	RIGHT JOIN tag ON question_tag.tag_id = tag.id
	GROUP BY tag_id,tag.name;"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def answer_accepted_reputation_up(cursor: RealDictCursor, answer_id: int):
    query = """ UPDATE users
    SET reputation = reputation + 15
    WHERE id in (SELECT user_id FROM answer WHERE id = (%s)); """
    cursor.execute(query, (answer_id,))


@database_common.connection_handler
def answer_unaccepted_reputation_down(cursor: RealDictCursor, answer_id: int):
    query = """ UPDATE users
    SET reputation = reputation - 15
    WHERE id in (SELECT user_id FROM answer WHERE id = (%s)); """
    cursor.execute(query, (answer_id,))