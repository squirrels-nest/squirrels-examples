from typing import Iterable
from squirrels import ModelDepsArgs, ModelArgs
from sklearn.linear_model import LinearRegression
import pandas as pd, numpy as np


def dependencies(sqrl: ModelDepsArgs) -> Iterable[str]:
    return ["dbv_weather_by_date", "dbv_ice_cream_sales"]


def main(sqrl: ModelArgs) -> pd.DataFrame:
    """
    Create federated models by joining/processing dependent database views and/or other federated models to
    form and return the result as a new pandas DataFrame.
    """
    df_weather = sqrl.ref("dbv_weather_by_date")
    df_ice_cream = sqrl.ref("dbv_ice_cream_sales")
    df_joined = df_weather.merge(df_ice_cream, on="date")

    ## Get ML model
    model: LinearRegression = sqrl.connections["ice_cream_regr_model"]
    
    ## Make prediction
    df_joined["temperature_c"] = df_joined["temperature_max"]
    prediction = model.predict(df_joined[["temperature_c"]].rename(columns={"temperature_c": "temp_c"}))
    df_joined["expected_profit"] = np.round(prediction, 2)

    ## Select columns
    df = df_joined[["date", "ice_cream_profits", "temperature_c", "expected_profit"]]
    return df
