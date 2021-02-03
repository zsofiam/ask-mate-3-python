import database_common
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

#
# def get_all_questions_from_file():
#     all_questions = util.get_dictionary_list_from_file(QUESTIONS_FILE_PATH)
#     return all_questions
#
#
# def get_questions_sorted(parameter, direction):
#     questions = get_all_questions_from_file()
#     if parameter == 'submission_time' or parameter == 'vote_number' or parameter == 'view_number':
#         sorted_questions = sort_by_number_parameter(questions, parameter, direction)
#     elif parameter == 'title' or parameter == 'message':
#         sorted_questions = sort_by_text_parameter(questions, parameter, direction)
#     else:
#         sorted_questions = sort_by_number_parameter(questions, 'submission_time', 'desc')
#     return sorted_questions
#
#
# def sort_by_number_parameter(questions, parameter, direction):
#     if direction == 'desc':
#         sorted_questions = sorted(questions, key=lambda k: int(k[parameter]), reverse=True)
#     else:
#         sorted_questions = sorted(questions, key=lambda k: int(k[parameter]))
#     return sorted_questions
#
#
# def sort_by_text_parameter(questions, parameter, direction):
#     if direction == 'desc':
#         sorted_questions = sorted(questions, key=lambda k: k[parameter], reverse=True)
#     else:
#         sorted_questions = sorted(questions, key=lambda k: k[parameter])
#     return sorted_questions
#
#
# def get_one_question(q_id):
#     all_questions = get_all_questions_from_file()
#     for question in all_questions:
#         if question['id'] == q_id:
#             return question


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
def write_answer(cursor: RealDictCursor, question_id: int, message: str, image: str) -> list:
    if image is not None:
        query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}', '{}');""".format(question_id, message, image)
        cursor.execute(query)
    else:
        query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message)
        VALUES (CURRENT_TIMESTAMP, 0, {}, '{}');""".format(question_id, message)
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
        SELECT question_id, image
        FROM answer
        WHERE id = {}""".format(answer_id)
    cursor.execute(query)
    return cursor.fetchone()


# def add_question(question, filename):
#     question_id = util.get_latest_id('question', LATEST_IDS)
#     question["id"] = question_id
#     question["submission_time"] = engine.get_timestamp()
#     question["vote_number"] = 0
#     question["view_number"] = 0
#     question['image'] = filename
#     questions = get_all_questions_from_file()
#     questions.append(question)
#     write_questions_to_file(questions)
#
#
# def write_questions_to_file(questions):
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#
#
# def modify_question(parameter_id, modifications):
#     questions = get_all_questions_from_file()
#     question = util.find_object_by_id(parameter_id, questions)
#     modified_question = util.add_modifications_to_object(question, modifications)
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#     return modified_question
#
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
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()


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


# def sort_by_number_parameter(questions, parameter, direction):
#     if direction == 'desc':
#         sorted_questions = sorted(questions, key=lambda k: int(k[parameter]), reverse=True)
#     else:
#         sorted_questions = sorted(questions, key=lambda k: int(k[parameter]))
#     return sorted_questions
#
#
# def sort_by_text_parameter(questions, parameter, direction):
#     if direction == 'desc':
#         sorted_questions = sorted(questions, key=lambda k: k[parameter], reverse=True)
#     else:
#         sorted_questions = sorted(questions, key=lambda k: k[parameter])
#     return sorted_questions
#
#
# def get_one_question(q_id):
#     all_questions = get_all_questions_from_file()
#     for question in all_questions:
#         if question['id'] == q_id:
#             return question
#
#
# def write_questions_to_file(questions):
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#
#
# def modify_question(parameter_id, modifications):
#     questions = get_all_questions_from_file()
#     question = util.find_object_by_id(parameter_id, questions)
#     modified_question = util.add_modifications_to_object(question, modifications)
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#     return modified_question
#