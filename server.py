from flask import Flask, render_template
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route('/list')
def route_list():
    questions_list = data_manager.get_questions_sorted_by_submission_date()
    return render_template('list.html', questions=questions_list)


if __name__ == "__main__":
    app.run()
