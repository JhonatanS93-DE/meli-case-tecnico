import pandas as pd
from datetime import timedelta

def generate_features(data):
    """
    Generate final dataset using:
    - prints from last week
    - aggregated views, clicks, payments, and amounts in previous 3 weeks
    """
    prints = data["prints"]
    taps = data["taps"]
    pays = data["pays"]

    # Convert timestamps
    prints["timestamp"] = pd.to_datetime(prints["timestamp"])
    taps["timestamp"] = pd.to_datetime(taps["timestamp"])
    pays["timestamp"] = pd.to_datetime(pays["timestamp"])

    max_date = prints["timestamp"].max()
    last_week = max_date - timedelta(days=7)
    three_weeks = max_date - timedelta(days=28)

    # Filter last week prints
    filtered_prints = prints[prints["timestamp"] >= last_week]

    def aggregate_events(df, event, column="timestamp", value_column=None):
        if value_column:
            df = df.groupby(["user_id", "value_prop_id"])[value_column].sum().reset_index()
        else:
            df = df.groupby(["user_id", "value_prop_id"]).size().reset_index(name=event)
        return df

    # Aggregates from last 3 weeks
    prior_prints = prints[(prints["timestamp"] < last_week) & (prints["timestamp"] >= three_weeks)]
    prior_taps = taps[(taps["timestamp"] < last_week) & (taps["timestamp"] >= three_weeks)]
    prior_pays = pays[(pays["timestamp"] < last_week) & (pays["timestamp"] >= three_weeks)]

    views = aggregate_events(prior_prints, "views_last_3_weeks")
    clicks = aggregate_events(prior_taps, "clicks_last_3_weeks")
    payments = aggregate_events(prior_pays, "payments_last_3_weeks")
    amounts = aggregate_events(prior_pays, "total_amount_last_3_weeks", value_column="amount")

    # Merge features
    merged = filtered_prints.merge(taps, how="left", on=["user_id", "value_prop_id", "timestamp"], suffixes=("", "_tap"))
    merged["was_clicked"] = ~merged["timestamp_tap"].isna()

    enriched = merged.drop(columns=["timestamp_tap"]).merge(views, how="left", on=["user_id", "value_prop_id"]) \
                     .merge(clicks, how="left", on=["user_id", "value_prop_id"]) \
                     .merge(payments, how="left", on=["user_id", "value_prop_id"]) \
                     .merge(amounts, how="left", on=["user_id", "value_prop_id"])

    enriched.fillna(0, inplace=True)
    return enriched
