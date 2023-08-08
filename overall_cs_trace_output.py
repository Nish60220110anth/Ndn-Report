from util import clean_file, get_dataframe, check_file_exist
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib


class CsTraceConfig:
    def __init__(self, _start, _interval, _end) -> None:
        self.start = _start
        self.interval = _interval
        self.end = _end

    def __str__(self) -> str:
        return "start: {0} interval: {1}".format(self.start, self.interval)


def add_row(df: pd.DataFrame, time, hit, miss):
    df[len(df)] = [time, hit, miss]


def get_file_name(file_name):
    name: str = os.path.basename(file_name)
    return name.split(".")[0]


def get_graph(df):
    matplotlib.use('cairo')
    plt.plot(df["Time"], df["Hits"])
    plt.show(True)


"""
ValueError: 'cario.png' is not a valid value for backend; supported values are 
['GTK3Agg', 'GTK3Cairo', 'GTK4Agg', 'GTK4Cairo', 'MacOSX', 'nbAgg', 'QtAgg', 
'QtCairo', 'Qt5Agg', 'Qt5Cairo', 'TkAgg', 'TkCairo', 'WebAgg', 'WX', 'WXAgg', 
'WXCairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template']
"""


def main(config: CsTraceConfig):
    file_name = "./traces/dyn-fib-cstrace.txt"

    if check_file_exist(file_name=file_name):
        clean_file(file_name=file_name)
        df = get_dataframe(file_name=file_name)

        if not df.empty:
            s = config.start + config.interval

            svalues = []
            hits = []
            misses = []

            while s <= config.end:
                hit = 0
                miss = 0

                for loc in range(0, len(df)):
                    if df.loc[loc]["Time"] == s:
                        if df.loc[loc]["Type"] == "CacheHits":
                            hit += df.loc[loc]["Packets"]
                        else:
                            miss += df.loc[loc]["Packets"]

                svalues.append(s)
                hits.append(hit)
                misses.append(miss)
                s += config.interval
            else:
                new_df = pd.DataFrame(
                    data={"Time": svalues, "Hits": hits, "Misses": misses})
                new_df.to_csv("./" + os.path.dirname(file_name) + "/" +
                              get_file_name(file_name=file_name) + "-modified.txt", index=False, sep="\t")

                matplotlib.use('cairo')
                plt.plot(new_df["Time"],new_df["Hits"])
                plt.savefig("./traces/graph.png")


if __name__ == "__main__":
    config = CsTraceConfig(0, 2, 40)
    main(config=config)
