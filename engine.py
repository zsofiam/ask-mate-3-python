import data_manager
import time


def get_timestamp():
    timestamp = int(time.time())
    return timestamp


def delete_answer(answer_id):
    question_id = ""
    image_name = ""
    answers = data_manager.get_all_answers()
    for answer in answers:
        if str(answer[0]) == str(answer_id):
            question_id = answer[3]
            image_name = answer[5]
            answers.remove(answer)
            break
    return answers, question_id, image_name


def delete_question(question_id):
    questions = data_manager.get_all_questions_from_file()
    image_name = ""
    for question in questions:
        if question['id'] == question_id:
            image_name = question['image']
            questions.remove(question)
            break
    return questions, image_name
