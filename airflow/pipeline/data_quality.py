from pipeline.utils import log

def run_quality_checks(df):
    if df.isnull().sum().sum() > 0:
        log("[WARN] Existen valores nulos.")
    else:
        log("No hay valores nulos.")

    if df.duplicated().any():
        log("[WARN] Existen registros duplicados.")
    else:
        log("No hay duplicados.")