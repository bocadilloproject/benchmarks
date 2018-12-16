import json
from benchmarks.config import Config
from benchmarks.manager import Manager
from pprint import pprint


def main():
    with open('config.json') as f:
        config = Config.from_json(json.loads(f.read()))

    manager = Manager(config)
    scores = manager.run()

    print(50 * "=")
    pprint(scores)


if __name__ == '__main__':
    main()
