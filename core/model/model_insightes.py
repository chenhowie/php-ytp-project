import eli5
import os
from eli5.sklearn import PermutationImportance
from matplotlib import pyplot as plt
from sklearn.inspection import PartialDependenceDisplay
import pickle


# 利用排序重要性分析參數影響預測的權重
def perimp(model_name, features, target):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    perm = PermutationImportance(model).fit(features, target)
    eli5.formatters.as_dataframe.explain_weights_df(perm, feature_names = features.columns.tolist()).to_csv("temp_data/perimptemp.csv")
    return "temp_data/perimptemp.csv"


#利用部分相依圖顯示參數影響預測的方式

def pdpd1d(model_name, features, target):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    arg = features.columns
    path='temp_data/partial dependence 1d'
    try:
        os.rmdir(path)
    except:
        pass
    for i in arg:
        disp1 = PartialDependenceDisplay.from_estimator(model, features, [i])
        plt.savefig(f"temp_data/partial dependence 1d/{i}.png")
    return "temp_data/partial dependence 1d"

#2D 部分相依圖

def pdpd2d(model_name, features, target, arg1, arg2):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    arg = features.columns
    path='temp_data/partial dependence 2d'
    try:
        os.rmdir(path)
    except:
        pass
    fig, ax = plt.subplots(figsize=(8, 6))
    f_names = [(arg1, arg2)]
    disp4 = PartialDependenceDisplay.from_estimator(model, features, f_names, ax=ax)
    plt.savefig(f"temp_data/partial dependence 2d/{arg1}-{arg2}.png")