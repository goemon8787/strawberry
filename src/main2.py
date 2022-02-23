# rollなし，roll_days = 1 による結果を見る

from Dataset import Dataset
from predict import predict
from Simulator import Simulator
from sklearn.metrics import mean_squared_error

PRICE_DATA_PATH = "./data/kk.csv"
HARVEST_DATA_PATH = "./data/harvest.csv"

roll_days = 5
move_days = 3
span = 10
n_input = 7
sim_start_year = 2020


def root_mean_squared_error(y_pred, y_test):
    return mean_squared_error(y_pred, y_test) ** (1 / 2)


def compare_result(max_result, fix_result, prop_result, farm):
    if farm == "h0":
        res_col = "h0_profit"
    else:
        res_col = "h1_profit"

    profit_max = max_result[res_col].sum()
    profit_fix = fix_result[res_col].sum()
    profit_prop = prop_result[res_col].sum()

    print("---------------------------")
    print("max result:  ", profit_max)
    print("fix result:  ", profit_fix)
    print("prop result: ", profit_prop)
    print("---------------------------")
    print("max - fix: ", profit_max - profit_fix)
    print("prop - max: ", profit_prop - profit_max)
    print("prop - fix: ", profit_prop - profit_fix)
    print("---------------------------")
    print("improve rate: ", (profit_max - profit_prop) / (profit_max - profit_fix))


if __name__ == "__main__":
    # データ読み込み
    dataset = Dataset(
        file_path=PRICE_DATA_PATH, roll_days=roll_days, span=span, n_input=n_input,
    )
    data_raw = dataset.make_train_test("raw")
    data_ma = dataset.make_train_test("ma")

    # 予測
    y_preds_raw = predict(data_raw, show_result=False)
    y_preds_ma = predict(data_ma, show_result=False)

    y_preds_raw, data_raw, data_c_raw = dataset.postprocess(y_preds_raw, mode="raw")
    y_preds_ma, data_ma, data_c_ma = dataset.postprocess(y_preds_ma, mode="ma")

    y_c_test = [d[3] for d in data_c_raw]
    min_len = min(list(map(len, y_c_test)))
    y_c_test = [yct[:min_len] for yct in y_c_test]

    raw_mses = []
    ma_mses = []
    for i in range(10):
        print("model", i + 1)

        raw_mse = mean_squared_error(y_preds_raw[i], y_c_test[i])
        ma_mse = mean_squared_error(y_preds_ma[i], y_c_test[i])

        print("  raw: ", raw_mse)
        print("   ma: ", ma_mse)

        raw_mses.append(raw_mse)
        ma_mses.append(ma_mse)

    print("sum raw mse: ", sum(raw_mses))
    print(" sum ma mse: ", sum(ma_mses))

    # sim = Simulator(
    #     y_preds=y_preds,
    #     data_c=data_c,
    #     df=dataset.df,
    #     harvest_data_path=HARVEST_DATA_PATH,
    #     sim_start_year=2020,
    #     move_days=move_days,
    #     span=span,
    #     n_input=n_input,
    # )

    # max_result = sim.simulate("max")
    # fix_result = sim.simulate("fix")
    # prop_result = sim.simulate("prop")

    # compare_result(max_result, fix_result, prop_result, farm="h0")
    # compare_result(max_result, fix_result, prop_result, farm="h1")

