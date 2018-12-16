import subprocess
from collections import defaultdict
from contextlib import contextmanager
from os.path import join, exists
from time import sleep

from psutil import Process

from benchmarks.config import Config, Test, Framework
from benchmarks.utils import wait_online, kill_recursively, \
    wait_offline


class Runner:

    def __init__(self, config: Config):
        self.config = config
        self.frameworks = config.frameworks
        self.tests = config.tests

    def get_python(self, framework: Framework) -> str:
        # TODO
        # - Create virtualenv
        # - Install dependencies
        # - Return path to virtualenv's Python executable
        return 'python'

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
            sleep(self.config.warmup_seconds)
            yield
        except TimeoutError as e:
            print(e)
            raise Exception(
                f"{script} failed to start the server at "
                f"{host}:{port} (framework: {framework.name})"
            )
        except Exception as e:
            print(e)
            raise Exception(
                f"{script} encountered an unknown error "
                f"(framework: {framework.name}"
            )
        finally:
            kill_recursively(Process(p.pid))
            try:
                wait_offline(self.config.host, self.config.port)
            except TimeoutError as e:
                print(e)
                raise Exception(
                    f"{script} failed to stop the server at "
                    f"{host}:{port} (framework: {framework.name})"
                )
            finally:
                sleep(self.config.warmup_seconds)

    def benchmark(self, script: str, framework: Framework, test: Test) -> int:
        with self.server(script, framework):
            # TODO run wrk
            return 0

    def run(self) -> dict:
        scores = defaultdict(defaultdict)

        for framework in self.frameworks:
            directory = join(self.config.frameworks_dir, framework.dirname)
            if not exists(directory):
                continue
            for test in self.tests:
                script_path = join(directory, test.filename)
                score = self.benchmark(script_path, framework, test)
                scores[test.name][framework.name] = score

        return self.format_scores(scores)

    @staticmethod
    def format_scores(scores: defaultdict) -> dict:
        formatted = {}
        for test, results in scores.items():
            formatted[test] = dict(results)
        return formatted
