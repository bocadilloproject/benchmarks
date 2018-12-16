from collections import defaultdict
from os.path import join, exists
from benchmarks.config import Config


class Runner:

    def __init__(self, config: Config):
        self.config = config
        self.frameworks = config.frameworks
        self.tests = config.tests

    def run(self) -> dict:
        scores = defaultdict(defaultdict)
        for framework in self.frameworks:
            directory = join(self.config.frameworks_dir, framework.dirname)
            if not exists(directory):
                continue
            for test in self.tests:
                # TODO get from running a script
                score = 0
                scores[test.name][framework.name] = score

        return self.format_scores(scores)

    @staticmethod
    def format_scores(scores: defaultdict) -> dict:
        formatted = {}
        for test, results in scores.items():
            formatted[test] = dict(results)
        return formatted
