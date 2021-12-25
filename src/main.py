from Dataset import Dataset
from predict import predict

if __name__ == "__main__":
    # データ読み込み
    dataset = Dataset("./data/kk.csv")
    data = dataset.data

    # 予測
    y_preds = predict(data)


    # モデルごとの予測データ数を揃える
    y_preds_min_len = min(list(map(len, y_preds)))
    y_preds_fix = []
    for p in y_preds:
        y_preds_fix.append(p[:y_preds_min_len])

    data_fix = []
    for d in data:
        X_train_fix = d[0].iloc[:y_preds_min_len]
        X_test_fix = d[1].iloc[:y_preds_min_len]
        y_train_fix = d[2].iloc[:y_preds_min_len]
        y_test_fix = d[3].iloc[:y_preds_min_len]
        data_fix.append((X_train_fix, X_test_fix, y_train_fix, y_test_fix))

    