import logging
import shutil
import subprocess
from collections import defaultdict
from contextlib import contextmanager
from os.path import join, exists, dirname
from time import sleep

from psutil import Process

from benchmarks.config import Config, Framework
from benchmarks.utils import (
    wait_online, kill_recursively, wait_offline, get_wrk_reqs_per_second,
)


class Runner:

    def __init__(self, config: Config):
        self.config = config
        self.frameworks = config.frameworks
        self.tests = config.tests
        self._logger = logging.getLogger("root")
        self._logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def _run(
        self, command: str, timeout: int = 30, **kwargs
    ) -> subprocess.Popen:
        self._logger.info(f"Running: %s", command)
        kwargs.setdefault("stdout", subprocess.DEVNULL)
        p = subprocess.Popen(command, shell=True, **kwargs)
        p.wait(timeout)
        return p

    def get_python(self, framework: Framework) -> str:
        env_dir = framework.name.replace(" ", "_").lower()
        env_path = join(self.config.virtualenvs_dir, env_dir)
        python = join(env_path, "bin", "python3")

        if not exists(env_path):
            self._run(f"python -m venv {env_path}")
            # Install dependencies
            pip = join(dirname(python), "pip")
            if framework.requirements:
                packages = " ".join(framework.requirements)
                self._run(f"{pip} install -U {packages}", timeout=60)

        return python

    def wait(self, framework: Framework, up=True):
        seconds = self.config.warmup_seconds
        action = "Warming up" if up else "Cooling down"
        self._logger.info(f"%s %s for %ss", action, framework.name, seconds)
        sleep(seconds)

    @contextmanager
    def server(self, script: str, framework: Framework):
        """Spawn and manage a process for the framework server."""
        python = self.get_python(framework)
        host = self.config.host
        port = self.config.port
        command = [python, script, host, str(port)]
        p = subprocess.Popen(command, stdout=subprocess.PIPE)

        try:
            wait_online(host, port)
            self.wait(framework, up=True)
            yield
        except TimeoutError as e:
            self._logger.exception(e)
            raise Exception(
                f"{script} failed to start the server at "
                f"{host}:{port} (framework: {framework.name})"
            )
        except Exception as e:
            self._logger.exception(e)
            raise Exception(
                f"{script} encountered an unknown error "
                f"(framework: {framework.name}"
            )
        finally:
            kill_recursively(Process(p.pid))
            try:
                wait_offline(self.config.host, self.config.port)
            except TimeoutError as e:
                self._logger.exception(e)
                raise Exception(
                    f"{script} failed to stop the server at "
                    f"{host}:{port} (framework: {framework.name})"
                )
            finally:
                self.wait(framework, up=False)

    def benchmark(self, script: str, framework: Framework) -> int:
        with self.server(script, framework):
            duration = self.config.wrk_duration
            cmd = (
                f"wrk "
                f"-c {self.config.wrk_concurrency} "
                f"-t {self.config.wrk_threads} "
                f"http://{self.config.address}/ "
                f"-d {duration}"
            )
            p = self._run(cmd, timeout=duration + 2, stdout=subprocess.PIPE)
            output = p.stdout.read().decode()
            return get_wrk_reqs_per_second(output)

    def run(self) -> dict:
        scores = defaultdict(defaultdict)

        for framework in self.frameworks:
            directory = join(self.config.frameworks_dir, framework.dirname)
            if not exists(directory):
                continue
            print()
            print(10 * "=", framework.name, 10 * "=")
            print()
            for test in self.tests:
                print(f"Starting test: {test.name}")
                print()
                script_path = join(directory, test.filename)
                score = self.benchmark(script_path, framework)
                scores[test.name][framework.name] = score

        return self.format_scores(scores)

    @staticmethod
    def format_scores(scores: defaultdict) -> dict:
        formatted = {}
        for test, results in scores.items():
            formatted[test] = dict(results)
        return formatted

    def clean(self):
        self._logger.info("Cleaning up…")
        try:
            shutil.rmtree(self.config.virtualenvs_dir)
        except FileNotFoundError:
            pass
