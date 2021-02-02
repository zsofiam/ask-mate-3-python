import csv
import engine
import util

from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    print(cursor.fetchall())
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT * 
        FROM question
        WHERE id = {};""".format(id)
    cursor.execute(query)
    print(cursor.fetchone())
    return cursor.fetchone()


@database_common.connection_handler
def get_questions_sorted(cursor: RealDictCursor, parameter: str, direction: str ) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY {} {};""".format(parameter, direction)
    cursor.execute(query)
    print(cursor.fetchall())
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor: RealDictCursor, question: dict, filename: str) -> list:
    question['image'] = filename
    query = """
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
    VALUES(CURRENT_TIMESTAMP, 0, 0, '{}', '{}', '{}';
    SELECT SCOPE_IDENTITY();)"""\
        .format(question["title"], question['message'], question['image'])
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
# def get_answers(q_id):
#     answers = []
#     csv_file = open(ANSWERS_FILE_PATH)
#     csv_answers = csv.DictReader(csv_file)
#     for answer in csv_answers:
#         if answer['question_id'] == q_id:
#             answers.append(answer)
#     return answers
#
#
# def write_answer(new_row):
#     with open(ANSWERS_FILE_PATH, 'a') as file:
#         file.write(new_row)
#         file.write("\n")
#
#
# def write_questions_to_file(questions):
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#
#
# def get_all_answers():
#     answers = []
#     with open(ANSWERS_FILE_PATH) as csv_file:
#         csv_answers = csv.reader(csv_file)
#         for answer_index, answer in enumerate(csv_answers):
#             if answer_index != 0:
#                 answers.append(answer)
#     return answers
#
#
# def write_all_answers(answers):
#     first_row = ','.join(ANSWER_HEADER)
#     first_row += "\n"
#     with open(ANSWERS_FILE_PATH, 'w') as file:
#         file.write(first_row)
#     with open(ANSWERS_FILE_PATH, 'a') as file:
#         for answer in answers:
#             new_row = ','.join(answer)
#             file.write(new_row)
#             file.write("\n")
#
#
# def modify_question(parameter_id, modifications):
#     questions = get_all_questions_from_file()
#     question = util.find_object_by_id(parameter_id, questions)
#     modified_question = util.add_modifications_to_object(question, modifications)
#     util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
#     return modified_question
#
#
# def get_answer_id():
#     answer_id = util.get_latest_id('answer', LATEST_IDS)
#     return answer_id
#
