from typing import List


class Config:

    frameworks_dir = 'frameworks'
    virtualenvs_dir = '/virtualenvs'
    host = '0.0.0.0'
    port = 8000
    warmup_seconds = 5

    def __init__(self, tests: List['Test'], frameworks: List['Framework']):
        self.tests = tests
        self.frameworks = frameworks

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


class Framework:
    def __init__(self, name: str, requirements: List[str], dirname: str):
        self.name = name
        self.requirements = requirements
        self.dirname = dirname


class Test:

    def __init__(self, name: str, filename: str):
        self.name = name
        self.filename = filename
