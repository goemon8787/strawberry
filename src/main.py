from Dataset import Dataset
from predict import predict
from Simulator import Simulator

PRICE_DATA_PATH = "./data/kk.csv"
HARVEST_DATA_PATH = "./data/harvest.csv"

roll_days = 5
move_days = 3
span = 10
n_input = 7
sim_start_year = 2020


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
        file_path=PRICE_DATA_PATH, roll_days=roll_days, span=span, n_input=n_input
    )
    data = dataset.make_train_test()

    # 予測
    y_preds = predict(data)

    y_preds, data, data_c = dataset.postprocess(y_preds)

    sim = Simulator(
        y_preds=y_preds,
        data_c=data_c,
        df=dataset.df,
        harvest_data_path=HARVEST_DATA_PATH,
        sim_start_year=2020,
        move_days=move_days,
        span=span,
        n_input=n_input,
    )

    max_result = sim.simulate("max")
    fix_result = sim.simulate("fix")
    prop_result = sim.simulate("prop")

    compare_result(max_result, fix_result, prop_result, farm="h0")
    compare_result(max_result, fix_result, prop_result, farm="h1")

    print()
