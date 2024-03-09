import pandas as pd
import os
import json
import pickle

def load_feature(path):  #返還資料的參數
    df = pd.read_csv(path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return list(df)

def load_mlmodel():
    with open("config.json", "r") as jfile:
        ff = json.load(jfile)
    return ff["model_list"]


def list_model():
    model_list = os.listdir("data/model")
    return model_list

