import data_manager, engine
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def main_page():
    return redirect("/list")


@app.route('/list')
def route_list():
    order_by = 'submission_time'
    order_direction = 'desc'
    args = request.args
    if 'order_by' in args:
        order_by= args["order_by"]
    if 'order_direction' in args:
        order_direction = args['order_direction']
    questions_list = data_manager.get_questions_sorted(order_by,order_direction)
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


@app.route("/add-question", methods=['GET', 'POST'])
def post_new_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        question = {"title": request.form["title"], "message": request.form["message"]}
        data_manager.add_question(question)
        return redirect("/question/"+ str(question["id"]))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == 'POST':
        modifications = {"title": request.form["title"], "message": request.form["message"]}
        modified_question = data_manager.modify_question(question_id, modifications)
        return redirect("/question/" + str(modified_question["id"]))
    question = data_manager.get_one_question(question_id)
    return render_template('edit_question.html', question=question)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answers, question_id = engine.delete_answer(answer_id)
    data_manager.write_all_answers(answers)
    return redirect("/question/" + question_id)


if __name__ == "__main__":
    app.run(
        debug=True
    )
