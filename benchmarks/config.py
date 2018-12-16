from typing import List


class Config:
    """Benchmark configuration."""

    frameworks_dir = 'frameworks'
    virtualenvs_dir = '/virtualenvs'
    host = '0.0.0.0'
    port = 8000
    warmup_seconds = 2

    wrk_duration = 15
    wrk_concurrency = 400
    wrk_threads = 12

    def __init__(self, tests: List['Test'], frameworks: List['Framework']):
        self.tests = tests
        self.frameworks = frameworks

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @classmethod
    def from_json(cls, json: dict) -> 'Config':
        tests = []
        for obj in json["tests"]:
            test = Test(name=obj["name"], filename=obj["filename"])
            tests.append(test)

        frameworks = []
        for obj in json["frameworks"]:
            framework = Framework(
                name=obj["name"],
                requirements=obj["requirements"],
                dirname=obj["dirname"],
            )
            frameworks.append(framework)

        return cls(tests=tests, frameworks=frameworks)

    def estimate_duration(self):
        each: int = 2 * self.warmup_seconds + self.wrk_duration
        total: int = each * len(self.frameworks) * len(self.tests)
        return total

    def show(self):
        print(
            "Selected frameworks:",
            ", ".join((fmk.name for fmk in self.frameworks))
        )
        minutes: int = round(self.estimate_duration() / 60, 1)
        print()
        print(f"This will take at least {minutes} minutes to run.")
        print("Please be patient.")
        print(50 * "-")


class Framework:
    def __init__(self, name: str, requirements: List[str], dirname: str):
        self.name = name
        self.requirements = requirements
        self.dirname = dirname


class Test:

    def __init__(self, name: str, filename: str):
        self.name = name
        self.filename = filename
