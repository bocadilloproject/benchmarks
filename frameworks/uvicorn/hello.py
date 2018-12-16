import sys
from multiprocessing import cpu_count
from os.path import dirname, join
from subprocess import Popen, DEVNULL, STDOUT


class App:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": b"Hello, World!",
        })


if __name__ == "__main__":
    cwd = dirname(__file__)
    gunicorn = join(dirname(sys.executable), "gunicorn")
    host, port = sys.argv[1], sys.argv[2]
    cmd = (
        f"{gunicorn} hello:App "
        f"-w {cpu_count()} "
        "-k uvicorn.workers.UvicornWorker "
        f"-b {host}:{port}"
    )
    p = Popen(cmd, cwd=cwd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    p.wait()
