import os

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


# 数量で重み付け
def ma_weighted(price, df):
    """
    Args:
        price (df.rolling): df.rolling.apply()を想定した価格列
        df: 重み列を取るための元df
    return:
        ma_w = 数量加重移動平均
    """

    df_price = df.loc[price.index, "価格"]
    df_num = df.loc[price.index, "数量"]

    ma_w = 0
    for p, n in zip(df_price, df_num):
        ma_w += n * p / df_num.sum()

    return ma_w


class Dataset:
    """
    データセットの成形，train，test，データの作成
    """

    def __init__(
        self,
        file_path,
        roll_days=5,
        start_test_idx=9426,
        span=10,
        n_input=7,
        rolling=True,
    ):
        """
        Args:
            file_path (str): データファイルのパス
            roll_days (int): 移動平均の日数
        """
        self.file_path = file_path
        self.roll_days = roll_days
        self.start_test_idx = start_test_idx

        self.span = span  # 何日分予測するか
        self.n_input = n_input  # 何日分入力するか

        self.df = self.preprocess()

        self.ma_w = self.ma_df()

    def preprocess(self):
        df_raw = pd.read_csv(self.file_path)

        # 全体のみを利用(産地名NaN)
        is_nan = [df_raw["産地名"][i] is df_raw["産地名"][0] for i in range(df_raw.shape[0])]
        df = df_raw[is_nan].copy()
        del_columns = ["産地名", "産地コード", "品目名", "品目コード", "対前日比（数量）", "対前日比（価格）"]
        df = df.drop(del_columns, axis=1).copy()

        # 曜日の処理
        dow = ["月", "火", "水", "木", "金", "土", "日"]
        df["曜日"] = [dow.index(dw) for dw in df["曜日"]]

        # 日にちの処理
        # timestamp型 → timedelta
        date = [
            str(df["年"].iloc[i])
            + "-"
            + str(df["月"].iloc[i])
            + "-"
            + str(df["日"].iloc[i])
            for i in range(df.shape[0])
        ]
        df["date"] = pd.to_datetime(date)
        df["days"] = [(date - df["date"][0]).days for date in df["date"]]
        df = df.drop("date", axis=1).copy()

        return df

    def ma_df(self):
        return (
            self.df["価格"]
            .rolling(self.roll_days)
            .apply(ma_weighted, args=(self.df,), raw=False)
            .dropna()
        )

    def make_train_test(self, mode="ma"):
        """
        mode (str): {"ma", "raw"}
        """

        if mode == "ma":
            df_train = self.ma_w[self.ma_w.index < self.start_test_idx].copy()
            df_test = self.ma_w[self.ma_w.index >= self.start_test_idx].copy()
        elif mode == "raw":
            df_for_compare = self.df["価格"].iloc[self.roll_days - 1 :]
            df_train = df_for_compare[df_for_compare.index < self.start_test_idx].copy()
            df_test = df_for_compare[df_for_compare.index >= self.start_test_idx].copy()

        date_train_raw = self.df.loc[df_train.index, ["年", "月", "日", "曜日"]].copy()
        date_test_raw = self.df.loc[df_test.index, ["年", "月", "日", "曜日"]].copy()

        # 学習データ作成
        # data = [4日後予測訓練データ, 5日後予測訓練データ, ..., 10日後予測訓練データ]

        # 入力データから予測対象日までの最短日数 = 輸送日数 + [1,2,3,4,5,6,7,...]
        data = []
        for sp in range(self.span):

            sp = sp + 1

            n_train = df_train.shape[0] - (self.n_input - 1) - sp

            X_train_idx = [np.arange(self.n_input) + i for i in range(n_train)]
            y_train_idx = [(self.n_input - 1) + sp + i for i in range(n_train)]

            date_train_idx = [i + (self.n_input - 1) for i in range(n_train)]

            n_test = df_test.shape[0] - (self.n_input - 1) - sp

            X_test_idx = [np.arange(self.n_input) + i for i in range(n_test)]
            y_test_idx = [(self.n_input - 1) + sp + i for i in range(n_test)]

            date_test_idx = [i + (self.n_input - 1) for i in range(n_test)]

            X_train = np.array([df_train.iloc[xt_i].values for xt_i in X_train_idx])

            y_train = np.array([df_train.iloc[yt_i] for yt_i in y_train_idx])

            X_test = np.array([df_test.iloc[xt_i].values for xt_i in X_test_idx])
            y_test = np.array([df_test.iloc[yt_i] for yt_i in y_test_idx])

            X_train = pd.DataFrame(X_train, columns=np.arange(self.n_input))
            X_test = pd.DataFrame(X_test, columns=np.arange(self.n_input))
            y_train = pd.Series(y_train)
            y_test = pd.Series(y_test)

            date_train = date_train_raw.iloc[date_train_idx].reset_index(drop=True)
            date_test = date_test_raw.iloc[date_test_idx].reset_index(drop=True)

            X_train = pd.concat([X_train, date_train], axis=1)
            X_test = pd.concat([X_test, date_test], axis=1)

            data.append((X_train, X_test, y_train, y_test))

        return data

    def postprocess(self, y_preds, mode="ma"):
        # モデルごとの予測データ数を揃える
        y_preds_min_len = min(list(map(len, y_preds)))
        y_preds_fix = []
        for p in y_preds:
            y_preds_fix.append(p[:y_preds_min_len])

        # 予測結果に合わせて学習，テストデータを揃える
        data_fix = []
        ma_df = self.make_train_test(mode)
        for d in ma_df:
            X_train_fix = d[0].iloc[:y_preds_min_len]
            X_test_fix = d[1].iloc[:y_preds_min_len]
            y_train_fix = d[2].iloc[:y_preds_min_len]
            y_test_fix = d[3].iloc[:y_preds_min_len]
            data_fix.append((X_train_fix, X_test_fix, y_train_fix, y_test_fix))

        data_c_fix = []
        raw_df = self.make_train_test("raw")
        for d in raw_df:
            X_train_fix = d[0].iloc[:y_preds_min_len]
            X_test_fix = d[1].iloc[:y_preds_min_len]
            y_train_fix = d[2].iloc[:y_preds_min_len]
            y_test_fix = d[3].iloc[:y_preds_min_len]
            data_c_fix.append((X_train_fix, X_test_fix, y_train_fix, y_test_fix))

        return (y_preds_fix, data_fix, data_c_fix)

