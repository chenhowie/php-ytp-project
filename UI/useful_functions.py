import pandas as pd
import os

def string_process(path: str, l: list, fileName: str):
    sl = []
    df = pd.read_csv(path)
    for i in range(len(l)):
        if l[i] == 0:
            sl.append(df.columns[i])
    df = df.drop(columns=sl)
    longFileName = os.path.join(os.path.abspath(os.path.dirname(path)), fileName)
    df.to_csv(longFileName)
    return longFileName