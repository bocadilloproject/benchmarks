import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load(filename) -> pd.DataFrame:
    return pd.read_csv(filename)


def main(filename):
    data = load(filename)
    sns.set(style="whitegrid")
    g = sns.catplot(x="framework", y="score", hue="concurrency", data=data,
                    height=6, kind="bar")
    g.despine(left=True)
    g.set_ylabels("Requests/sec")
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])
