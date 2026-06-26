import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch
from datetime import datetime


def make_fake_taxi_df(n=500, seed=42):
    rng = np.random.default_rng(seed)
    pickup = pd.date_range("2022-01-01", periods=n, freq="10min")
    duration_minutes = rng.uniform(2, 50, size=n)
    dropoff = pickup + pd.to_timedelta(duration_minutes, unit="m")
    return pd.DataFrame(
        {
            "lpep_pickup_datetime": pickup,
            "lpep_dropoff_datetime": dropoff,
            "PULocationID": rng.integers(1, 265, size=n),
            "DOLocationID": rng.integers(1, 265, size=n),
            "trip_distance": rng.uniform(0.5, 20, size=n),
        }
    )


@pytest.fixture(autouse=True)
def mock_read_parquet():
    with patch("pandas.read_parquet", side_effect=lambda url: make_fake_taxi_df()):
        yield
