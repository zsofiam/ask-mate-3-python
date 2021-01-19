import data_manager
import time


def generate_answer_id(q_id):
    answers = data_manager.get_answers(q_id)
    next_id = 0
    for answer in answers:
        next_id = int(answer['id'])
    next_id += 1
    return next_id


def generate_questions_id():
    questions = data_manager.get_all_questions_from_file()
    next_id = 0
    for question in questions:
        next_id = int(question['id'])
    next_id += 1
    return next_id


def get_timestamp():
    timestamp = int(time.time())
    return timestamp