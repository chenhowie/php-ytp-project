import pandas as pd
import os
from sklearn.cluster import KMeans

"""
待辦

使用者用位置切割而不是關鍵字

"""

# 字串切割 (檔案路徑, 資料行數, 關鍵字)
def string_split(path, col, key): 
    #path 是資料的路徑
    #col 要改的欄位
    #key 分割關鍵字
    df = pd.read_csv(path)
    df_ = df[col].str.split(key)
    df = df.drop(columns=[col])
    for i in range(len(df_[0])):
        df[f'{col}_s{i}'] = df_.str[i]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv(os.path.join(os.path.abspath(os.path.dirname(path)), "temp.csv"))
    return os.path.join(os.path.abspath(os.path.dirname(path)), "temp.csv")

# 分群
def cluster(path, col, group):
    df = pd.read_csv(path)
    df_ = df[col]
    temp = KMeans(n_clusters=group).fit_predict(df[['f2']])
    df[f'{col}_c{group}'] = temp
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.to_csv(os.path.join(os.path.abspath(os.path.dirname(path)), "temp.csv"))
    return os.path.join(os.path.abspath(os.path.dirname(path)), "temp.csv")
