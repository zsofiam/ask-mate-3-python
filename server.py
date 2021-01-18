from flask import Flask, render_template
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route('/list')
def route_list():
    all_questions = data_manager.get_all_questions()

    return render_template('list.html', questions=all_questions)

if __name__ == "__main__":
    app.run()
