import json
from datetime import datetime
from os import makedirs
from os.path import join

from benchmarks.config import Config
from benchmarks.runner import Runner


def main():
    with open("config.json") as f:
        config = Config.from_json(json.loads(f.read()))

    config.show()

    runner = Runner(config)
    results = runner.run()
    runner.clean()

    print()
    print(50 * "=")
    print()

    makedirs("results", exist_ok=True)
    filename = join("results", datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    filename = filename + ".csv"
    results.to_csv(filename, header=True, index=False)
    print("Results saved to", filename)
    print("Done")


if __name__ == "__main__":
    main()
