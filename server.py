import data_manager
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def main_page():
    return redirect('/list')


@app.route('/list')
def route_list():
    order_by = 'submission_time'
    order_direction = 'desc'
    args = request.args
    if 'order_by' in args:
        order_by = args["order_by"]
    if 'order_direction' in args:
        order_direction = args['order_direction']
    questions_list = data_manager.get_questions_sorted(order_by, order_direction)
    return render_template('list.html', questions=questions_list)


@app.route("/question/<question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers(question_id)
    question_comments = data_manager.get_question_comment(question_id)
    return render_template('q_and_a.html',question=question, answers=answers, comments=question_comments)


@app.route("/add-question", methods=['GET', 'POST'])
def post_new_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        question = {"title": request.form["title"], "message": request.form["message"]}
        if request.files["file"]:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        question['image'] = filename
        question_from_database = data_manager.add_question(question)
        return redirect("/question/" + str(question_from_database["id"]))


@app.route("/question/<int:question_id>/new-answer", methods=['GET', 'POST'])
def post_new_answer(question_id):
    if request.method == 'GET':
        return render_template('new_answer.html', question_id=str(question_id))
    else:
        if request.files["file"]:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        message = request.form['new_message']
        data_manager.write_answer(question_id, message, filename)
        return redirect("/question/" + str(question_id))


@app.route("/question/<int:question_id>/new_comment", methods=['GET', 'POST'])
def post_new_comment(question_id):
    if request.method == 'GET':
        return render_template('new_comment.html', question_id=str(question_id))
    else:
        comment = request.form['new_comment']
        data_manager.write_comment(question_id, comment)
        return redirect("/question/" + str(question_id))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        modifications = {"title": request.form["title"], "message": request.form["message"]}
        if request.files["file"]:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            modifications["image"] = filename
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            try:
                old_file = question["image"]
                os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], old_file))
            except (TypeError, FileNotFoundError):
                pass
        else:
            modifications["image"] = None
        data_manager.modify_question(question_id, modifications)
        return redirect("/question/" + str(question["id"]))
    question = data_manager.get_question_by_id(question_id)
    return render_template('edit_question.html', question=question)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    answer_ids = data_manager.get_question_answers(question_id)
    filename = data_manager.get_question_by_id(question_id)['image']
    for answer_id in answer_ids:
        delete_answer(answer_id['id'], True)
    data_manager.delete_question(question_id)
    try:
        os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    except (FileNotFoundError, TypeError):
        print("No file was removed!")
    return redirect("/list")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id, del_question):
    filename = data_manager.get_answer_data(answer_id)['image']
    question_id = data_manager.get_answer_data(answer_id)['question_id']
    data_manager.delete_answer(answer_id)
    if filename is not None:
        os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    if del_question:
        return
    return redirect("/question/" + str(question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect("/list")


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect("/list")


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def vote_up_answer(answer_id):
    data_manager.vote_up_answer(answer_id)
    question_id = data_manager.get_answer_data(answer_id)['question_id']
    return redirect("/question/" + str(question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def vote_down_answer(answer_id):
    data_manager.vote_down_answer(answer_id)
    question_id = data_manager.get_answer_data(answer_id)['question_id']
    return redirect("/question/" + str(question_id))


if __name__ == "__main__":
    app.run(
        debug=True
    )
