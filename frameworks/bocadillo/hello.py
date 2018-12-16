import sys
from multiprocessing import cpu_count
from os.path import join, dirname
from subprocess import PIPE, Popen

from bocadillo import API

api = API()

i = 0


@api.route("/")
async def hello(req, res):
    global i
    i += 1
    print(i)
    res.text = "Hello, World!"


if __name__ == "__main__":
    cwd = dirname(__file__)
    gunicorn = join(dirname(sys.executable), "gunicorn")
    host, port = sys.argv[1], sys.argv[2]
    cmd = (
        f"{gunicorn} hello:api "
        f"-w {cpu_count()} "
        f"-k uvicorn.workers.UvicornWorker "
        f"-b {host}:{port}"
    )
    p = Popen(cmd, shell=True, cwd=cwd, stdout=PIPE, stderr=PIPE)
    p.wait()
