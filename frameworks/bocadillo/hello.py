import sys
from multiprocessing import cpu_count
from os.path import dirname, join
from subprocess import STDOUT, DEVNULL, Popen

from bocadillo import API

api = API()


@api.route("/")
async def hello(req, res):
    res.text = "Hello, World!"


if __name__ == "__main__":
    cwd = dirname(__file__)
    gunicorn = join(dirname(sys.executable), 'gunicorn')
    host, port = sys.argv[1], sys.argv[2]
    cmd = (
        f"{gunicorn} hello:api "
        f"-w {2 * cpu_count() + 1} "
        "-k uvicorn.workers.UvicornWorker "
        f"-b {host}:{port}"
    )
    p = Popen(cmd, cwd=cwd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    p.wait()
