import json
from benchmarks.config import Config
from benchmarks.runner import Runner
from pprint import pprint


def main():
    with open('config.json') as f:
        config = Config.from_json(json.loads(f.read()))

    config.show()

    runner = Runner(config)
    scores = runner.run()
    runner.clean()

    print()
    print(50 * "=")
    print()

    pprint(scores)


if __name__ == '__main__':
    main()
