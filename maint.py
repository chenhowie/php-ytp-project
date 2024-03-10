import core.main_window.main_window as func1
import core.data_process.feature_engineering.feature_extract as func2
import core.model.train_model as func3
import core.model.model_insights as func4

if __name__ == '__main__':

    # #取得參數 (回傳參數)
    # print(f"features : {func1.load_feature(path)}")

    # 資料處裡-字串處理 (回傳位置)
    # print(func2.string_split(path, 'f1', "-"))

    # 資料處裡-分群 (回傳位置)
    # print(func2.cluster(path, 'f2', 3))

    # 建立模型
    print(func3.train_model(training_features="core/demo/temp_feature.csv", training_target="core/demo/temp_target.csv", model_name="test", model="Decision_Tree"))

    # 模型列表
    # print(f"model list : {func1.list_model()}")

    # # 使用模型預測新資料
    print(func3.predict_model("core/demo/temp_feature.csv", "test"))

    # # 使用 permutation importance 分析模型 (回傳.csv檔路徑)
    print(func4.perimp("test", "core/demo/temp_feature.csv", "core/demo/temp_target.csv"))

    # # Partial Dependence display 1D
    print(func4.pdpd1d("test", "core/demo/temp_feature.csv", "core/demo/temp_target.csv"))

    # # Partial Dependence display 2D
    print(func4.pdpd2d("test", "core/demo/temp_feature.csv", "core/demo/temp_target.csv", "F1", "F2"))