import pandas as pd
import os
import json
import pickle

def train_model(training_features, training_target, model_name, model="Decision_Tree"):
    if (model=="Decision_Tree"):
        feature = pd.read_csv(training_features)
        target = pd.read_csv(training_target)
        feature = feature.loc[:, ~feature.columns.str.contains('^Unnamed')]
        target = target.loc[:, ~target.columns.str.contains('^Unnamed')]
        # feature_max_ = feature.max(axis=0)
        # feature_min_ = feature.min(axis=0)
        # target_max_ = target.max(axis=0)
        # target_min_ = target.min(axis=0)
        X_train = feature.sample(frac=0.7)
        X_train = X_train.sort_index()
        X_valid = feature.drop(X_train.index)
        X_valid = X_valid.sort_index()
        Y_valid = target.drop(X_train.index)
        Y_valid = Y_valid.sort_index()
        Y_train = target.drop(Y_valid.index)
        Y_train = Y_train.sort_index()
        # X_train = feature
        # Y_train = target
        # X_train = (X_train - feature_min_) / (feature_max_ - feature_min_)
        # X_valid = (X_valid - feature_min_) / (feature_max_ - feature_min_)
        # Y_train = (Y_train - target_min_) / (target_max_ - target_min_)
        # Y_valid = (Y_valid - target_min_) / (target_max_ - target_min_)
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(X_train, Y_train)
        from sklearn.metrics import mean_absolute_error
        predicted = model.predict(X_valid)
        pickle.dump(model, open(f"data/model/{model_name}", 'wb'))
        return f"success! mean absolute error : {mean_absolute_error(Y_valid, predicted)}"
    else:
        return ValueError(f"Model not found : \"{model_name}\"")
    
def predict_model(predicting_features, model_name):
    model = pickle.load(open(f"data/model/{model_name}", 'rb'))
    feature = pd.read_csv(predicting_features)
    feature = feature.loc[:, ~feature.columns.str.contains('^Unnamed')]
    predicted = model.predict(feature)
    predicted = pd.DataFrame(predicted)
    predicted.to_csv(f"data/prediction/temp.csv")
    return "data/prediction/temp.csv"
