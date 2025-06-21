import pandas as pd
from datetime import timedelta
from pipeline.utils import log

def generate_features(data):
    # Desempaquetar los dataframes
    prints = data["prints"]
    taps = data["taps"]
    pays = data["pays"]

    # Fase 1: Conversión de fechas
    prints["timestamp"] = pd.to_datetime(prints["timestamp"])
    taps["timestamp"] = pd.to_datetime(taps["timestamp"])
    pays["timestamp"] = pd.to_datetime(pays["timestamp"])

    # Determinar la fecha máxima y calcular las ventanas temporales
    max_date = prints["timestamp"].max()
    last_week = max_date - timedelta(days=7)
    three_weeks = max_date - timedelta(days=28)
    log(f"Máxima fecha detectada en prints: {max_date.date()}")

    # Fase 2: Filtro de la última semana
    filtered_prints = prints[prints["timestamp"] >= last_week]

    # Fase 3: Agregación de eventos en ventana móvil
    def aggregate_events(df, event, column="timestamp", value_column=None):
        if value_column:
            df = df.groupby(["user_id", "value_prop_id"])[value_column].sum().reset_index()
        else:
            df = df.groupby(["user_id", "value_prop_id"]).size().reset_index(name=event)
        return df

    # Datos de las 3 semanas previas a cada print
    prior_prints = prints[(prints["timestamp"] < last_week) & (prints["timestamp"] >= three_weeks)]
    prior_taps = taps[(taps["timestamp"] < last_week) & (taps["timestamp"] >= three_weeks)]
    prior_pays = pays[(pays["timestamp"] < last_week) & (pays["timestamp"] >= three_weeks)]

    # Generar métricas agregadas
    views = aggregate_events(prior_prints, "views_last_3_weeks")
    clicks = aggregate_events(prior_taps, "clicks_count")
    payments = aggregate_events(prior_pays, "payments_last_3_weeks")
    amounts = aggregate_events(prior_pays, "total_amount_last_3_weeks", value_column="amount")

    # Fase 4: Enriquecimiento del print
    merged = filtered_prints.merge(taps, how="left", on=["user_id", "value_prop_id", "timestamp"], suffixes=("", "_tap"))
    merged["was_clicked"] = ~merged["timestamp_tap"].isna()

    # Fase 5: Unificación final de métricas
    enriched = merged.drop(columns=["timestamp_tap"])\
                     .merge(views, how="left", on=["user_id", "value_prop_id"])\
                     .merge(clicks, how="left", on=["user_id", "value_prop_id"])\
                     .merge(payments, how="left", on=["user_id", "value_prop_id"])\
                     .merge(amounts, how="left", on=["user_id", "value_prop_id"])

    # Fase 6: Limpieza y retorno
    enriched.fillna(0, inplace=True)
    log("Dataset enriquecido generado.")
    return enriched