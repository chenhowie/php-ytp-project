import pandas as pd
import os
import json

def string_process(path: str, l: list, fileName: str):
    sl = []
    df = pd.read_csv(path)
    for i in range(len(l)):
        if l[i] == 0:
            sl.append(df.columns[i])
    df = df.drop(columns=sl)
    df.to_csv(fileName)

def JSON_WRITE(M: dict, path: str):
    with open(path, mode = "w", encoding = "utf-8") as file:
        json.dump(M, file, indent = 4)

def JSON_READ(path: str):
    M = dict()
    try:
        with open(path, mode = "r", encoding = "utf-8") as file:
            M = json.load(file)
    except: 
        pass
    return M

