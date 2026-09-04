"""
Feature engineering for FootPrint crowd forecasting.

Each function is documented for hackathon judges — these features help
XGBoost capture temporal patterns that raw dates alone cannot express.
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Columns used as model inputs after engineering
FEATURE_COLUMNS = [
    "lag_1",
    "lag_7",
    "lag_30",
    "rolling_mean_7",
    "rolling_mean_30",
    "day_of_week",
    "month",
    "is_holiday",
    "is_weekend",
    "weather_temp",
    "weather_condition_encoded",
    "destination_encoded",
]

TARGET_COLUMN = "footfall_count"


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lag features: yesterday's footfall predicts tomorrow's crowd.

    - lag_1:  Same weekday pattern from yesterday (short-term momentum)
    - lag_7:  Same day last week (captures weekly seasonality)
    - lag_30: Same day ~1 month ago (captures monthly/seasonal trends)
    """
    df = df.sort_values(["destination_id", "date"]).copy()
    for lag in (1, 7, 30):
        df[f"lag_{lag}"] = df.groupby("destination_id")["footfall_count"].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rolling averages smooth out daily noise and reveal trend direction.

    - rolling_mean_7:  Short-term trend (recent week average)
    - rolling_mean_30: Long-term baseline (recent month average)
    """
    df = df.sort_values(["destination_id", "date"]).copy()
    for window in (7, 30):
        df[f"rolling_mean_{window}"] = (
            df.groupby("destination_id")["footfall_count"]
            .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
        )
    return df


def encode_categoricals(
    df: pd.DataFrame,
    weather_encoder: LabelEncoder | None = None,
    dest_encoder: LabelEncoder | None = None,
    fit: bool = True,
) -> tuple[pd.DataFrame, LabelEncoder, LabelEncoder]:
    """
    Encode weather_condition and destination_id as integers for XGBoost.

    Returns the transformed dataframe plus fitted encoders (needed at inference).
    """
    df = df.copy()
    if weather_encoder is None:
        weather_encoder = LabelEncoder()
    if dest_encoder is None:
        dest_encoder = LabelEncoder()

    if fit:
        df["weather_condition_encoded"] = weather_encoder.fit_transform(df["weather_condition"])
        df["destination_encoded"] = dest_encoder.fit_transform(df["destination_id"])
    else:
        # Handle unseen categories gracefully at inference time
        df["weather_condition_encoded"] = df["weather_condition"].map(
            {c: i for i, c in enumerate(weather_encoder.classes_)}
        ).fillna(0).astype(int)
        df["destination_encoded"] = df["destination_id"].map(
            {c: i for i, c in enumerate(dest_encoder.classes_)}
        ).fillna(0).astype(int)

    return df, weather_encoder, dest_encoder


def build_features(
    df: pd.DataFrame,
    weather_encoder: LabelEncoder | None = None,
    dest_encoder: LabelEncoder | None = None,
    fit_encoders: bool = True,
) -> tuple[pd.DataFrame, LabelEncoder, LabelEncoder]:
    """
    Full feature pipeline: lags → rolling stats → calendar flags → encodings.

    Drops rows with NaN lags (first 30 days per destination).
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    df = add_lag_features(df)
    df = add_rolling_features(df)

    # Calendar features already in raw data; ensure correct types
    df["is_holiday"] = df["is_holiday"].astype(int)
    df["is_weekend"] = df["is_weekend"].astype(int)
    df["day_of_week"] = df["day_of_week"].astype(int)
    df["month"] = df["month"].astype(int)

    df, weather_encoder, dest_encoder = encode_categoricals(
        df, weather_encoder, dest_encoder, fit=fit_encoders
    )

    # Remove rows where lag_30 is missing (need 30 days of history)
    df = df.dropna(subset=["lag_30"]).reset_index(drop=True)
    return df, weather_encoder, dest_encoder


def get_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Extract model-ready feature matrix."""
    return df[FEATURE_COLUMNS].copy()
