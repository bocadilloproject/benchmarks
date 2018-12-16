from typing import List, NamedTuple


class Config:
    """Benchmark configuration."""

    def __init__(
        self,
        tests: List['Test'],
        frameworks: List['Framework'],
        benches: List['Bench'],
        frameworks_dir: str,
        virtualenvs_dir: str,
        host: str,
        port: int,
        warmup_seconds: int,
    ):
        self.tests = tests
        self.frameworks = frameworks
        self.benches = benches
        self.frameworks_dir = frameworks_dir
        self.virtualenvs_dir = virtualenvs_dir
        self.host = host
        self.port = port
        self.warmup_seconds = warmup_seconds

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @classmethod
    def from_json(cls, json: dict) -> 'Config':
        tests = []
        for obj in json.pop("tests", []):
            tests.append(Test(**obj))

        frameworks = []
        for obj in json.pop("frameworks", []):
            if not obj.pop("enabled", True):
                continue
            frameworks.append(Framework(**obj))

        benches = []
        for obj in json.pop("wrk", []):
            benches.append(Bench(**obj))

        return cls(tests=tests, frameworks=frameworks, benches=benches, **json)

    def estimate_duration(self):
        each: int = sum(
            bench.duration + 2 * self.warmup_seconds for bench in self.benches
        )

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
        print()


class Framework(NamedTuple):
    name: str
    requirements: List[str]
    dirname: str


class Test(NamedTuple):
    name: str
    filename: str


class Bench(NamedTuple):
    concurrency: int
    threads: int
    duration: int

    @property
    def id(self) -> str:
        return f"{self.concurrency}_{self.threads}_{self.duration}"

    def show(self):
        print("Concurrency:", self.concurrency)
        print("Threads:", self.threads)
        print("Duration:", self.duration)
