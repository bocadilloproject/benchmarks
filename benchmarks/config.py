from typing import List


class Config:
    """Benchmark configuration."""

    def __init__(
            self,
            tests: List['Test'],
            frameworks: List['Framework'],
            frameworks_dir: str,
            virtualenvs_dir: str,
            host: str,
            port: int,
            warmup_seconds: int,
            wrk_duration: int,
            wrk_concurrency: int,
            wrk_threads: int,
    ):
        self.tests = tests
        self.frameworks = frameworks
        self.frameworks_dir = frameworks_dir
        self.virtualenvs_dir = virtualenvs_dir
        self.host = host
        self.port = port
        self.warmup_seconds = warmup_seconds
        self.wrk_duration = wrk_duration
        self.wrk_concurrency = wrk_concurrency
        self.wrk_threads = wrk_threads

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @classmethod
    def from_json(cls, json: dict) -> 'Config':
        tests = []
        for obj in json.pop("tests", []):
            test = Test(name=obj["name"], filename=obj["filename"])
            tests.append(test)

        frameworks = []
        for obj in json.pop("frameworks", []):
            if not obj.get("enabled", True):
                continue
            framework = Framework(
                name=obj["name"],
                requirements=obj["requirements"],
                dirname=obj["dirname"],
            )
            frameworks.append(framework)

        return cls(tests=tests, frameworks=frameworks, **json)

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
