import subprocess
import sys
from multiprocessing import cpu_count
from os.path import join, dirname


def run_gunicorn(cwd: str, app: str, worker: str):
    gunicorn = join(dirname(sys.executable), "gunicorn")
    worker_class = {
        "uvicorn": "uvicorn.workers.UvicornWorker",
        "meinheld": "'egg:meinheld#gunicorn_worker'",
    }[worker]
    host, port = sys.argv[1], sys.argv[2]
    cmd = (
        f"{gunicorn} {app} "
        f"-w {2 * cpu_count() + 1} "
        f"-k {worker_class} "
        f"-b {host}:{port}"
    )
    p = subprocess.Popen(
        cmd, cwd=cwd, shell=True,
        # Do not capture stdout at all (=> increase in speed)
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    p.wait()
