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

def get_bitset(keys: list, selected: list):
    bitset = []
    for i in keys:
        bitset.append(0)
    for i in selected:
        if not (i in keys):
            return [], False
        for j in range(len(keys)):
            if keys[j] == i:
                bitset[j] = 1
                break
    return bitset, True

def get_selected(keys: list, bitset: list):
    if len(keys) != len(bitset):
        return [], False
    selected = []
    for i in range(len(keys)):
        if bitset[i] == 1:
            selected.append(keys[i])
    return selected, True

def get_all(path: str, selected: list):
    df = None
    try:
        df = pd.read_csv(path)
    except:
        return [], [], False
    keys = df.columns.copy()
    bitset, succeed = get_bitset(keys, selected)
    if not succeed:
        return [], [], False
    return keys, bitset, True


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

