import json
from benchmarks.config import Config
from benchmarks.runner import Runner
from pprint import pprint


def main():
    with open('config.json') as f:
        config = Config.from_json(json.loads(f.read()))

    runner = Runner(config)
    scores = runner.run()

    print(50 * "=")
    pprint(scores)


if __name__ == '__main__':
    main()
