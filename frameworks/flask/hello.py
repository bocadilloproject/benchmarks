import sys
from multiprocessing import cpu_count
from os.path import join, dirname
from subprocess import Popen, DEVNULL, STDOUT

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!", 200


if __name__ == "__main__":
    cwd = dirname(__file__)
    gunicorn = join(dirname(sys.executable), 'gunicorn')
    host, port = sys.argv[1], sys.argv[2]
    cmd = (
        f"{gunicorn} hello:app "
        f"-w {cpu_count()} "
        f"--worker-class='egg:meinheld#gunicorn_worker' "
        f"-b {host}:{port}"
    )
    p = Popen(cmd, cwd=cwd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    p.wait()
