from flask import Flask
import flask

app = Flask(__name__)


@app.route('/')
def index():
    context = {}
    return flask.render_template("index.html", **context)


if __name__ == '__main__':
    app.run()
