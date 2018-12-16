from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!", 200


if __name__ == "__main__":
    from os.path import dirname
    from frameworks.common import run_gunicorn

    run_gunicorn(
        cwd=dirname(__file__),
        app="hello:app",
        worker="meinheld",
    )
