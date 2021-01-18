import data_manager
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


if __name__ == "__main__":
    app.run(
        debug=True
    )
