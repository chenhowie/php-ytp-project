import eli5
import os
from eli5.sklearn import PermutationImportance
from matplotlib import pyplot as plt
from sklearn.inspection import PartialDependenceDisplay
import pickle
import pandas as pd
import shutil


# 利用排序重要性分析參數影響預測的權重
def perimp(model_name, features, target):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    features = pd.read_csv(features)
    target = pd.read_csv(target)
    features = features.loc[:, ~features.columns.str.contains('^Unnamed')]
    target = target.loc[:, ~target.columns.str.contains('^Unnamed')]
    perm = PermutationImportance(model).fit(features, target)
    eli5.formatters.as_dataframe.explain_weights_df(perm, feature_names = features.columns.tolist()).to_csv("core/temp_data/perimptemp.csv")
    return "core/temp_data/perimptemp.csv"


#利用部分相依圖顯示參數影響預測的方式

def pdpd1d(model_name, features, target):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    features = pd.read_csv(features)
    target = pd.read_csv(target)
    features = features.loc[:, ~features.columns.str.contains('^Unnamed')]
    target = target.loc[:, ~target.columns.str.contains('^Unnamed')]
    arg = features.columns
    path='core/temp_data/partial_dependence_1d'
    try:
        shutil.rmtree(path)(path)
    except:
        pass
    os.mkdir(path)
    for i in arg:
        disp1 = PartialDependenceDisplay.from_estimator(model, features, [i])
        plt.savefig(f"core/temp_data/partial_dependence_1d/{i}.png")
    return "core/temp_data/partial_dependence_1d"

#2D 部分相依圖

def pdpd2d(model_name, features, target, arg1, arg2):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    features = pd.read_csv(features)
    target = pd.read_csv(target)
    features = features.loc[:, ~features.columns.str.contains('^Unnamed')]
    target = target.loc[:, ~target.columns.str.contains('^Unnamed')]
    arg = features.columns
    path='core/temp_data/partial_dependence_2d'
    try:
        shutil.rmtree(path)(path)
    except:
        pass
    os.mkdir(path)
    fig, ax = plt.subplots(figsize=(8, 6))
    f_names = [(arg1, arg2)]
    disp4 = PartialDependenceDisplay.from_estimator(model, features, f_names, ax=ax)
    plt.savefig(f"core/temp_data/partial_dependence_2d/{arg1}-{arg2}.png")
    return "core/temp_data/partial_dependence_2d"