import pandas as pd
import numpy as np


class Simulator:
    def __init__(
        self,
        y_preds,
        data_c,
        df,
        harvest_data_path,
        sim_start_year,
        move_days,
        span,
        start_test_idx=9426,
        n_input=7,
    ):
        """
        元データ，学習データ，テストデータをもとにシミュレーションを実施
        """

        self.y_preds = y_preds
        self.data_c = data_c
        self.y_c_test = [dcf[3] for dcf in data_c]
        self.df = df

        self.datelist_input, self.datelist_output = self.make_datelist(
            start_test_idx, span, n_input
        )

        self.date_df = pd.DataFrame(
            {
                "input_date": self.datelist_input.reset_index(drop=True),
                "output1": self.datelist_output[0].reset_index(drop=True),
                "output2": self.datelist_output[1].reset_index(drop=True),
                "output3": self.datelist_output[2].reset_index(drop=True),
                "output4": self.datelist_output[3].reset_index(drop=True),
                "output5": self.datelist_output[4].reset_index(drop=True),
                "output6": self.datelist_output[5].reset_index(drop=True),
                "output7": self.datelist_output[6].reset_index(drop=True),
                "output8": self.datelist_output[7].reset_index(drop=True),
                "output9": self.datelist_output[8].reset_index(drop=True),
                "output10": self.datelist_output[9].reset_index(drop=True),
            }
        )

        self.pred_df = pd.DataFrame(
            {
                "input_date": self.datelist_input.reset_index(drop=True),
                "output1": self.y_preds[0],
                "output2": self.y_preds[1],
                "output3": self.y_preds[2],
                "output4": self.y_preds[3],
                "output5": self.y_preds[4],
                "output6": self.y_preds[5],
                "output7": self.y_preds[6],
                "output8": self.y_preds[7],
                "output9": self.y_preds[8],
                "output10": self.y_preds[9],
            }
        )

        self.test_df = pd.DataFrame(
            {
                "input_date": self.datelist_input.reset_index(drop=True),
                "output1": self.y_c_test[0],
                "output2": self.y_c_test[1],
                "output3": self.y_c_test[2],
                "output4": self.y_c_test[3],
                "output5": self.y_c_test[4],
                "output6": self.y_c_test[5],
                "output7": self.y_c_test[6],
                "output8": self.y_c_test[7],
                "output9": self.y_c_test[8],
                "output10": self.y_c_test[9],
            }
        )

        self.valid_test_df = self.make_valid_df(self.test_df, move_days, span)
        self.valid_pred_df = self.make_valid_df(self.pred_df, move_days, span)

        self.harvest_df_raw = self.make_harvest_df(harvest_data_path, sim_start_year)

        self.harvest_df_test = pd.merge(self.harvest_df_raw, self.valid_test_df)
        self.harvest_df_date = pd.merge(self.harvest_df_raw, self.date_df)
        self.harvest_df_pred = pd.merge(self.harvest_df_raw, self.valid_pred_df)

    def make_harvest_df(self, harvest_data_path, sim_start_year):
        harvest_df_raw = pd.read_csv(harvest_data_path, index_col=0)
        bools = harvest_df_raw.month > 10
        years = []
        for bool in bools:
            years.append(sim_start_year if bool else sim_start_year + 1)

        harvest_df_raw["year"] = years

        date = [
            str(harvest_df_raw["year"].iloc[i])
            + "-"
            + str(harvest_df_raw["month"].iloc[i])
            + "-"
            + str(harvest_df_raw["day"].iloc[i])
            for i in range(harvest_df_raw.shape[0])
        ]

        harvest_df_raw["date"] = pd.to_datetime(date)

        harvest_df_raw = harvest_df_raw.drop(["month", "day", "year"], axis=1)

        harvest_df_raw["date"] = harvest_df_raw["date"] + pd.Timedelta(days=6)

        input_days = []
        for hd in harvest_df_raw["date"]:
            diff_days = (self.valid_test_df["input_date"] - hd).dt.days
            diff_days = diff_days[diff_days >= 0]
            min_deltatime = diff_days.min()
            input_day = hd + pd.Timedelta(days=min_deltatime)
            input_days.append(input_day)
        harvest_df_raw["input_date"] = input_days

        return harvest_df_raw

    def make_datelist(self, start_test_idx, span, n_input):
        df_test_raw = self.df.loc[start_test_idx:].copy()
        # 予測のもとになった入力データの最後の日の日付
        # 最も有効データ数の多い1日後の予測をするモデルに合わせる
        datelist = pd.Series(
            [
                pd.to_datetime(
                    str(int(d["年"])) + "/" + str(int(d["月"])) + "/" + str(int(d["日"]))
                )
                for _, d in df_test_raw.iterrows()
            ]
        )

        datelist_input = pd.Series(
            [
                pd.to_datetime(
                    str(int(d["年"])) + "/" + str(int(d["月"])) + "/" + str(int(d["日"]))
                )
                for _, d in self.data_c[0][1].iterrows()
            ]
        )

        # 予測の際の正解データの日付
        # 最初を合わせる
        datelist_output = [datelist[(n_input - 1) :][n + 1 :] for n in range(span)]
        # 最後を合わせる
        do_len_min = min(list(map(len, datelist_output)))
        datelist_output = [do[:do_len_min] for do in datelist_output]

        # inputも最後を合わせる
        datelist_input = datelist_input[:do_len_min]

        return datelist_input, datelist_output

    def make_valid_df(self, raw_df, move_days, span):
        """
        有効データの抽出
        """

        bool_df1 = pd.DataFrame(
            np.array(
                [
                    (self.date_df[o_col] - self.date_df["input_date"]).dt.days <= span
                    for o_col in self.date_df.columns[1:]
                ]
            ).T,
            columns=raw_df.columns[1:],
        )
        bool_df2 = pd.DataFrame(
            np.array(
                [
                    move_days
                    < (self.date_df[o_col] - self.date_df["input_date"]).dt.days
                    for o_col in self.date_df.columns[1:]
                ]
            ).T,
            columns=raw_df.columns[1:],
        )
        bool_df = bool_df1 & bool_df2
        bool_df = pd.concat([self.date_df["input_date"], bool_df.astype(int)], axis=1)

        valid_df = raw_df.copy()
        valid_df.iloc[:, 1:] = raw_df.iloc[:, 1:] * bool_df.iloc[:, 1:]

        return valid_df

    def simulate(self, mode):
        """
        mode (str): {"max", "fix", "prop"}
        """
        if mode == "prop":
            harvest_df = self.harvest_df_pred.iloc[:, :4].copy()
        elif mode == "max" or mode == "fix":
            harvest_df = self.harvest_df_test.iloc[:, :4].copy()
        else:
            print('please check mode: {"max", "fix", "prop"}')
            return None

        prices = []
        dates = []
        for hdt in self.harvest_df_test.index:
            if mode == "prop":
                price = self.harvest_df_test.iloc[
                    hdt, np.argmax(self.harvest_df_pred.iloc[hdt, 4:]) + 4
                ]
                date = self.harvest_df_date.iloc[
                    hdt, np.argmax(self.harvest_df_pred.iloc[hdt, 4:]) + 4
                ]
            elif mode == "fix":
                price = self.harvest_df_test.iloc[hdt, 4:][
                    self.harvest_df_test.iloc[hdt, 4:] > 0
                ][0]
                output = self.harvest_df_test.iloc[hdt, 4:][
                    self.harvest_df_test.iloc[hdt, 4:] > 0
                ].index[0]
                date = self.harvest_df_date.iloc[hdt][output]
            elif mode == "max":
                price = np.max(self.harvest_df_test.iloc[hdt, 4:])
                date = self.harvest_df_date.iloc[
                    hdt, np.argmax(self.harvest_df_test.iloc[hdt, 4:]) + 4
                ]
            prices.append(price)
            dates.append(date)

        harvest_df["selling_price"] = prices
        harvest_df["selling_date"] = dates

        harvest_df["day_delta"] = harvest_df["selling_date"] - harvest_df["date"]

        harvest_df["h0_profit"] = harvest_df["h0"] * harvest_df["selling_price"]
        harvest_df["h1_profit"] = harvest_df["h1"] * harvest_df["selling_price"]

        return harvest_df
