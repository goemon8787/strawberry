import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def root_mean_squared_error(y_pred, y_test):
    return mean_squared_error(y_pred, y_test) ** (1 / 2)


def predict(data):
    y_preds = []
    for i in range(data.__len__()):
        X_train, X_test, y_train, y_test = (
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3],
        )

        model = lgb.LGBMRegressor(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = root_mean_squared_error(y_test, y_pred)
        print(rmse)

        ape = sum(abs((y_test - y_pred) / y_test))
        mape = ape / y_test.shape[0]
        print(mape)

        y_preds.append(y_pred)

    return y_preds

    
