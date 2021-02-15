
import data_manager
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route('/search')
def main_page():
    results = []
    results_answers = []
    word = ''
    query_string = request.args
    if 'q' in query_string and query_string['q'] != '':
        word = query_string['q']
        results = data_manager.search(word)
        results_answers = data_manager.search_answers(word)
    questions = data_manager.get_latest_five_questions()
    return render_template('index.html', questions=questions, results=results, results_answers=results_answers,
                           word=word)


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
    tags = data_manager.get_tags_by_question(question_id)
    comments = data_manager.get_comment(question_id)
    return render_template('q_and_a.html', question=question, answers=answers, tags=tags, comments=comments)


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
        modifications = {'message': request.form['new_message'], 'image': filename}
        data_manager.write_answer(question_id, modifications)
        return redirect("/question/" + str(question_id))


@app.route("/question/<int:question_id>/new-tag", methods=['GET', 'POST'])
def add_new_tag(question_id):
    all_tags = data_manager.get_all_tags()
    if request.method == 'GET':
        tags = data_manager.get_tags_by_question(question_id)
        return render_template('new_tag.html', question_id=str(question_id), all_tags=all_tags, tags=tags)
    else:
        new_tag = request.form["new-tag"]
        data_manager.remove_tags_from_question(question_id)
        for tag in all_tags:
            tag_id = str(tag["id"])
            tag_name = tag["name"]
            if tag_id in request.form.keys() and request.form[tag_id] == tag_name:
                data_manager.add_tag_to_question(tag_id, question_id)
        if new_tag:
            new_tag_saved = data_manager.save_tag(new_tag)
            data_manager.add_tag_to_question(new_tag_saved["id"], question_id)
        return redirect("/question/" + str(question_id))


@app.route("/question/<int:question_id>/new_comment", methods=['GET', 'POST'])
def post_new_comment(question_id):
    if request.method == 'GET':
        return render_template('new_comment.html', question_id=str(question_id))
    else:
        comment = request.form['new_comment']
        data_manager.write_comment(question_id, comment)
        return redirect("/question/" + str(question_id))


@app.route("/comment/<id>/<question_id>/delete")
def delete_comment(id, question_id):
    data_manager.delete_comment_by_id(id)
    return redirect("/question/" + str(question_id))


@app.route("/comment/<question_id>/<id>/edit", methods=["GET", "POST"])
def edit_comment(id, question_id):
    if request.method == 'GET':
        comment = data_manager.get_comment_message_by_id(id)
        return render_template('edit_comment.html', comment=comment)
    else:
        text = {"comment": request.form["new-message"]}
        data_manager.update_comment(id, text)
        return redirect("/question/" + str(question_id))


@app.route("/question/<int:question_id>/tag/<int:tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.remove_tag(question_id, tag_id)
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
    data_manager.remove_tags_from_question(question_id)
    data_manager.delete_comments_by_question_id(question_id)
    data_manager.delete_answers_by_question_id(question_id)
    filename = data_manager.get_question_by_id(question_id)['image']
    data_manager.delete_question(question_id)
    try:
        os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    except (FileNotFoundError, TypeError):
        print("No file was removed!")
    return redirect("/")


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    filename = data_manager.get_answer_data(answer_id)['image']
    question_id = data_manager.get_answer_data(answer_id)['question_id']
    comment_ids = data_manager.get_comment_id_by_answer(answer_id)
    for comment in comment_ids:
        data_manager.delete_comment_by_id(comment['id'])
    data_manager.delete_answer(answer_id)
    try:
        os.remove(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    except (FileNotFoundError, TypeError):
        pass
    return redirect("/question/" + str(question_id))


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    datas = data_manager.get_answer_data(answer_id)
    if request.method == 'GET':
        return render_template('edit_answer.html', answer_id=str(answer_id), datas=datas)
    else:
        if request.files["new-file"]:
            file = request.files["new-file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        modifications = {'message': request.form['new-message'], 'image': filename}
        data_manager.modify_answer(answer_id, modifications)
        return redirect("/question/" + str(datas['question_id']))


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect("/")


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect("/")


@app.route('/question/<question_id>/answer/<answer_id>/new_comment', methods=["GET", "POST"])
def post_new_answer_comment(answer_id, question_id):
    if request.method == 'GET':
        return render_template('new_answer_comment.html', answer_id=str(answer_id), question_id=str(question_id))
    else:
        comment = request.form['new_comment']
        data_manager.write_answer_comment(question_id, answer_id, comment)
        return redirect("/question/" + str(question_id))


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

