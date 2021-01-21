import csv
import engine
import util


QUESTIONS_FILE_PATH = 'sample_data/question.csv'
ANSWERS_FILE_PATH = "sample_data/answer.csv"
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
LATEST_IDS = "sample_data/latest_ids.txt"
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions_from_file():
    all_questions = util.get_dictionary_list_from_file(QUESTIONS_FILE_PATH)
    return all_questions


def get_questions_sorted(parameter, direction):
    questions = get_all_questions_from_file()
    if parameter == 'submission_time' or parameter == 'vote_number' or parameter == 'view_number':
        sorted_questions = sort_by_number_parameter(questions, parameter, direction)
    elif parameter == 'title' or parameter == 'message':
        sorted_questions = sort_by_text_parameter(questions, parameter, direction)
    else:
        sorted_questions = sort_by_number_parameter(questions, 'submission_time', 'desc')
    return sorted_questions


def sort_by_number_parameter(questions, parameter, direction):
    if direction == 'desc':
        sorted_questions = sorted(questions, key=lambda k: int(k[parameter]), reverse=True)
    else:
        sorted_questions = sorted(questions, key=lambda k: int(k[parameter]))
    return sorted_questions


def sort_by_text_parameter(questions, parameter, direction):
    if direction == 'desc':
        sorted_questions = sorted(questions, key=lambda k: k[parameter], reverse=True)
    else:
        sorted_questions = sorted(questions, key=lambda k: k[parameter])
    return sorted_questions


def get_one_question(q_id):
    all_questions = get_all_questions_from_file()
    for question in all_questions:
        if question['id'] == q_id:
            return question


def get_answers(q_id):
    answers = []
    csv_file = open(ANSWERS_FILE_PATH)
    csv_answers = csv.DictReader(csv_file)
    for answer in csv_answers:
        if answer['question_id'] == q_id:
            answers.append(answer)
    return answers


def write_answer(new_row):
    with open(ANSWERS_FILE_PATH, 'a') as file:
        file.write(new_row)
        file.write("\n")


def add_question(question, filename):
    question_id = util.get_latest_id('question', LATEST_IDS)
    question["id"] = question_id
    question["submission_time"] = engine.get_timestamp()
    question["vote_number"] = 0
    question["view_number"] = 0
    question['image'] = filename
    questions = get_all_questions_from_file()
    questions.append(question)
    write_questions_to_file(questions)


def write_questions_to_file(questions):
    util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)


def get_all_answers():
    answers = []
    with open(ANSWERS_FILE_PATH) as csv_file:
        csv_answers = csv.reader(csv_file)
        for answer_index, answer in enumerate(csv_answers):
            if answer_index != 0:
                answers.append(answer)
    return answers


def write_all_answers(answers):
    first_row = ','.join(ANSWER_HEADER)
    first_row += "\n"
    with open(ANSWERS_FILE_PATH, 'w') as file:
        file.write(first_row)
    with open(ANSWERS_FILE_PATH, 'a') as file:
        for answer in answers:
            new_row = ','.join(answer)
            file.write(new_row)
            file.write("\n")


def modify_question(parameter_id, modifications):
    questions = get_all_questions_from_file()
    question = util.find_object_by_id(parameter_id, questions)
    modified_question = util.add_modifications_to_object(question, modifications)
    util.write_dictionary_list_to_file(questions, QUESTIONS_FILE_PATH, QUESTIONS_HEADER)
    return modified_question


def get_answer_id():
    answer_id = util.get_latest_id('answer', LATEST_IDS)
    return answer_id

