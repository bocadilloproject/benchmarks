import socket
from psutil import Process, NoSuchProcess
from time import time, sleep


def wait_online(host: str, port: int, timeout: int = 10) -> None:
    """Wait until the server is available by trying to connect to it."""
    sock = socket.socket()
    sock.settimeout(timeout)
    count_down = timeout
    while count_down > 0:
        start_time = time()
        try:
            sock.connect((host, port))
            sock.close()
            return
        except OSError:
            sleep(0.001)
            count_down -= time() - start_time
    sock.close()
    raise TimeoutError(
        f"Server is taking too long (> {timeout}s) to get online."
    )


def wait_offline(host: str, port: int, timeout: int = 10) -> None:
    count_down = timeout
    while count_down > 0:
        start_time = time()
        with socket.socket() as sock:
            try:
                sock.settimeout(1)
                sock.connect((host, port))
                sleep(0.1)
                count_down -= time() - start_time
            except OSError:
                return
    raise TimeoutError(f"Server is still running after {timeout}s.")


def kill_recursively(p: Process):
    """Kill a process and all its children."""
    children = p.children()
    if children:
        for child in children:
            kill_recursively(child)
    try:
        p.kill()
    except NoSuchProcess:
        pass
