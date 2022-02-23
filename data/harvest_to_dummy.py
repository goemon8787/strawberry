import pandas as pd
import numpy as np

if __name__ == "__main__":
    harvest = pd.read_csv("./data/harvest_raw.csv", index_col=0)
    harvest["h0"] = 100
    harvest["h1"] = 200
    print(harvest)
    harvest.to_csv("./data/harvest.csv")
