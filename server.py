import data_manager, engine
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def main_page():
    data_manager.add_question({
        "title": "Egyes",
        "message": "Egyes számú kérdés"
    }, "image23.png")
    data_manager.get_questions()
    data_manager.get_question_by_id(1)
    return redirect('/list')


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
        if request.files["file"]:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ""
        new_answer = [str(data_manager.get_answer_id()),
                      str(engine.get_timestamp()),
                      '0',
                      str(question_id),
                      request.form['new_message'],
                      filename]
        new_row = ','.join(new_answer)
        data_manager.write_answer(new_row)
        return redirect("/question/"+question_id)

#gittestcomment
@app.route("/add-question", methods=['GET', 'POST'])
def post_new_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        question = {"title": request.form["title"], "message": request.form["message"]}
        if request.files["file"]:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ""
        question["id"] = data_manager.add_question(question, filename)
        return redirect("/question/"+ str(question["id"]))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == 'POST':
        file = request.files["file"]
        filename = secure_filename(file.filename)
        if filename:
            modifications = {"title": request.form["title"],
                             "message": request.form["message"],
                             "image": filename}
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            question = data_manager.get_one_question(question_id)
            old_file = question["image"]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_file))
        else:
            modifications = {"title": request.form["title"], "message": request.form["message"]}
        modified_question = data_manager.modify_question(question_id, modifications)
        return redirect("/question/" + str(modified_question["id"]))
    question = data_manager.get_one_question(question_id)
    return render_template('edit_question.html', question=question)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answers, question_id, filename = engine.delete_answer(answer_id)
    if filename is not "":
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data_manager.write_all_answers(answers)
    return redirect("/question/" + question_id)


@app.route('/vote_counter/<question_id>', methods=['POST'])
def vote_counter(question_id):
    questions = data_manager.get_all_questions_from_file()
    for question in questions:
        if question['id'] == question_id:
            question_votenumber = int(question["vote_number"]) + 1
            question["vote_number"] = str(question_votenumber)
    print(question)
    data_manager.write_questions_to_file(questions)
    return redirect("/list")

@app.route('/vote_decounter/<question_id>', methods=['POST'])
def vote_decounter(question_id):
    questions = data_manager.get_all_questions_from_file()
    for question in questions:
        if question['id'] == question_id:
            question_votenumber = int(question["vote_number"]) - 1
            question["vote_number"] = str(question_votenumber)
    print(question)
    data_manager.write_questions_to_file(questions)
    return redirect("/list")

@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    questions, filename = engine.delete_question(question_id)
    if filename is not "":
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data_manager.write_questions_to_file(questions)
    return redirect("/list")


if __name__ == "__main__":
    app.run(
        debug=True
    )

