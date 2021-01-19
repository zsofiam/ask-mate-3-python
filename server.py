import data_manager, engine
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def main_page():
    return redirect("/list")


@app.route('/list')
def route_list():
    questions_list = data_manager.get_questions_sorted_by_submission_date()
    return render_template('list.html', questions=questions_list)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_one_question(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template('q_and_a.html', question=question, answers=answers)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_new_answer(question_id):
    if request.method == 'GET':
        return render_template('new_answer.html', question_id=question_id)
    else:
        # id, submission_time, vote_number, question_id, message, image
        new_answer = [str(engine.generate_answer_id(question_id)),
                      str(engine.get_timestamp()),
                      '0',
                      str(question_id),
                      request.form['new_message'],
                      ""]
        new_row = ','.join(new_answer)
        data_manager.write_answer(new_row)
        return redirect("/question/"+question_id)


if __name__ == "__main__":
    app.run(
        debug=True
    )
