import os
import pandas as pd
import numpy as np
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

    df_price = df.loc[price.index, '価格']
    df_num = df.loc[price.index, '数量']
    
    ma_w = 0
    for p, n in zip(df_price, df_num):
        ma_w += n * p/df_num.sum()

    return ma_w



class Datasets:
    """
    データセットの成形，train，test，データの作成
    """
    def __init__(self, file_path, roll_days=5):
        """
        Args:
            file_path (str): データファイルのパス
            roll_days (int): 移動平均の日数
        """
        self.file_path = file_path
        self.roll_days = roll_days

        self.df = self.preprocess()

        self.ma_w5 = self.ma_df()

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
        date = [str(df["年"].iloc[i])+"-"+str(df["月"].iloc[i])+"-" +
                str(df["日"].iloc[i]) for i in range(df.shape[0])]
        df["date"] = pd.to_datetime(date)
        # df = df.drop(date_columns, axis=1).copy()
        df["days"] = [(date - df["date"][0]).days for date in df["date"]]
        df = df.drop("date", axis=1).copy()

        return df

    def ma_df(self):
        return self.df["価格"].rolling(self.roll_days).apply(ma_weighted, args=(self.df,), raw=False)

if __name__ == "__main__":
    data = Datasets("../data/kk.csv")
    print()