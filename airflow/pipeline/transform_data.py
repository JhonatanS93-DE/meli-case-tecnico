import pandas as pd
from datetime import timedelta
from pipeline.utils import log

def generate_features(data):
    # Validación inicial
    if not isinstance(data, dict):
        raise TypeError("Se esperaba un diccionario con los dataframes.")

    expected_keys = {"prints", "taps", "pays"}
    if not expected_keys.issubset(data.keys()):
        raise ValueError(f"Faltan claves esperadas en los datos: {expected_keys - data.keys()}")

    prints = data["prints"]
    taps = data["taps"]
    pays = data["pays"]

    # Renombrar columnas clave si es necesario
    for df, name in [(prints, "prints"), (taps, "taps"), (pays, "pays")]:
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"{name} no es un DataFrame.")
        if 'value_prop' in df.columns:
            df.rename(columns={'value_prop': 'value_prop_id'}, inplace=True)
            log(f"[INFO] Columna 'value_prop' renombrada a 'value_prop_id' en {name}")
        if 'pay_date' in df.columns:
            df.rename(columns={'pay_date': 'timestamp'}, inplace=True)
            log(f"[INFO] Columna 'pay_date' renombrada a 'timestamp' en {name}")

    # Verificar columna 'timestamp'
    for name, df in [("prints", prints), ("taps", taps), ("pays", pays)]:
        if 'timestamp' not in df.columns:
            log(f"[ERROR] El DataFrame '{name}' no contiene la columna 'timestamp'. Columnas: {df.columns.tolist()}")
            raise ValueError(f"El DataFrame '{name}' no contiene la columna 'timestamp'.")

    # Conversión de fechas
    for name, df in [("prints", prints), ("taps", taps), ("pays", pays)]:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df.dropna(subset=["timestamp"], inplace=True)
        log(f"[INFO] Fechas convertidas en {name}")

    # Calcular fechas límite
    max_date = prints["timestamp"].max()
    last_week = max_date - timedelta(days=7)
    three_weeks = max_date - timedelta(days=28)
    log(f"Máxima fecha detectada en prints: {max_date.date()}")

    # Filtro temporal
    filtered_prints = prints[prints["timestamp"] >= last_week]

    # Agregaciones
    def aggregate_events(df, event, value_column=None):
        if df.empty:
            return pd.DataFrame(columns=["user_id", "value_prop_id", event])
        if value_column:
            if value_column not in df.columns:
                log(f"[WARN] La columna '{value_column}' no está en el DataFrame. Se omite agregación '{event}'.")
                return pd.DataFrame(columns=["user_id", "value_prop_id", event])
            df = df.groupby(["user_id", "value_prop_id"])[value_column].sum().reset_index(name=event)
        else:
            df = df.groupby(["user_id", "value_prop_id"]).size().reset_index(name=event)
        return df

    # Filtrar históricos
    prior_prints = prints[(prints["timestamp"] < last_week) & (prints["timestamp"] >= three_weeks)]
    prior_taps = taps[(taps["timestamp"] < last_week) & (taps["timestamp"] >= three_weeks)]
    prior_pays = pays[(pays["timestamp"] < last_week) & (pays["timestamp"] >= three_weeks)]

    # Métricas
    views = aggregate_events(prior_prints, "views_last_3_weeks")
    clicks = aggregate_events(prior_taps, "clicks_count")
    payments = aggregate_events(prior_pays, "payments_last_3_weeks")
    amounts = aggregate_events(prior_pays, "total_amount_last_3_weeks", value_column="amount")

    # Enriquecimiento
    taps_renamed = taps.rename(columns={"timestamp": "timestamp_tap"})
    merged = filtered_prints.merge(
        taps_renamed,
        how="left",
        left_on=["user_id", "value_prop_id", "timestamp"],
        right_on=["user_id", "value_prop_id", "timestamp_tap"]
    )
    merged["was_clicked"] = ~merged["timestamp_tap"].isna()

    # Unión final
    enriched = merged.drop(columns=["timestamp_tap"], errors="ignore") \
        .merge(views, how="left", on=["user_id", "value_prop_id"]) \
        .merge(clicks, how="left", on=["user_id", "value_prop_id"]) \
        .merge(payments, how="left", on=["user_id", "value_prop_id"]) \
        .merge(amounts, how="left", on=["user_id", "value_prop_id"])

    enriched.fillna(0, inplace=True)
    log("Dataset enriquecido generado exitosamente.")
    return enriched
