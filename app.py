from flask import Flask
from data_retrieval.Main import get_fixture_over_2


app = Flask(__name__)


@app.route('/')
def hello_world():

    # results = get_fixture_over_2()
    return get_fixture_over_2()


if __name__ == '__main__':
    app.run()
