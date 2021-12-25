"""
This is the script to concat 4 files per city.
"""

import codecs
import os
from pathlib import Path

import pandas as pd

# 作業ディレクトリの定義
root_path = Path("/home/yamashitakeisuke/Documents/strawberry/")
os.chdir(root_path)

data_path = root_path.joinpath(Path("./data/amedas/"))


def check_n_files():
    """
    args:
        None
    return:
        true if the number of files is correct else false.
    """

    dir_list = os.listdir(data_path)

    n_all_files = 0
    for dir in dir_list:
        n_files = len(os.listdir(data_path.joinpath(dir)))
        if n_files != 4:
            print(dir)
        n_all_files += n_files

    return n_all_files == len(dir_list) * 4


def parse_csv(filepath):
    """
    args:
        filepath (pathlib.Path): a path of csv file
    return:
        df (pandas.DataFrame): a DataFrame of csv
    """

    with codecs.open(filepath, "r", "Shift-JIS", "ignore") as bfile:

        # 値の読み取り
        df = pd.read_table(bfile, delimiter=",", skiprows=6, index_col=0)

    with codecs.open(filepath, "r", "Shift-JIS", "ignore") as bfile:
        # 列名の読み取り
        columns = bfile.readlines()

    # 列名へのの処理
    columns = columns[:6]
    columns = [col[:-2] for col in columns]

    # 県名の保存
    file_name = set(columns[2].split(","))
    file_name = list(file_name)[1]

    # 主要ラベル
    labels_set = sorted(
        list(set(columns[3].split(","))), key=columns[3].split(",").index
    )

    # 補助ラベル
    sub_labels = columns[5].split(",")

    # 全ラベルをvalueに合わせて結合
    labels = []
    for sl in sub_labels:
        if sl == "":
            labels.append(labels_set.pop(0))
        else:
            labels.append(sl)

    # dfとラベルを結合
    if df.shape[1] != len(labels[1:]):
        print("Length error: ", filepath)

    df.columns = labels[1:]
    df.index.name = labels[0]

    return df, file_name


def concat_files(pr_path):
    """
    args:
        pr_path (pathlib.Path): folder path
    return:
        df (pandas.DataFrame): concat data
    """

    filelist = os.listdir(pr_path)
    df = None

    for file in filelist:
        filepath = Path(pr_path.joinpath(Path(file)))

        df_temp, fname = parse_csv(filepath)

        if df is None:
            df = pd.DataFrame([], columns=df_temp.columns)
        df = pd.concat([df, df_temp], axis=0)

    return df, fname


if __name__ == "__main__":
    pr_list = [dir for dir in os.listdir(data_path) if data_path.joinpath(dir).is_dir()]

    fnames = []
    k = 0
    for pr in pr_list:
        pr_path = data_path.joinpath(pr)
        df, fname = concat_files(pr_path)
        # "現象なし情報", "均質情報", "品質情報" をdrop
        try:
            df = df.drop(columns="現象なし情報")
        except KeyError:
            print("Key Error1: ", fname, pr)

        try:
            df = df.drop(columns="品質情報")
        except KeyError:
            print("Key Error2: ", fname, pr)

        try:
            df = df.drop(columns="均質番号")
        except KeyError:
            print("Key Error3: ", fname, pr)

        df.to_csv(data_path.joinpath(fname + ".csv"))
        fnames.append(fname)
        k += 1

    print(len(fnames))
    print(k)
