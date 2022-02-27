from flask import Flask, render_template
from data_retrieval.Main import get_fixture_over_2
from data_retrieval.test import convert_stats

app = Flask(__name__)


@app.route('/')
def hello_world():

    convert_stats()
    results = get_fixture_over_2()

    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
