import csv

QUESTIONS_FILE_PATH = 'sample_data/question.csv'
ANSWERS_FILE_PATH = "sample_data/answer.csv"
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_all_questions_from_file():
    all_questions = []
    with open(QUESTIONS_FILE_PATH) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            all_questions.append(row)
    return all_questions


def get_questions_sorted(parameter, direction):
    questions = get_all_questions_from_file()
    if parameter == 'submission_time' or parameter == 'vote_number' or parameter == 'view_number':
        sorted_questions = sort_by_number_parameter(questions, parameter, direction)
    else:
        sorted_questions = sort_by_text_parameter(questions, parameter, direction)
    return sorted_questions


def sort_by_number_parameter(questions, parameter, direction):
    if direction == 'desc':
        sorted_questions = sorted(questions, key = lambda  k: int(k[parameter]), reverse=True)
    else:
        sorted_questions = sorted(questions, key = lambda  k: int(k[parameter]))
    return sorted_questions


def sort_by_text_parameter(questions, parameter, direction):
    if direction == 'desc':
        sorted_questions = sorted(questions, key = lambda  k: k[parameter], reverse=True)
    else:
        sorted_questions = sorted(questions, key = lambda  k: k[parameter])
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
