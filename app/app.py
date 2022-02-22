from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    # results = get_fixture_over_2()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
