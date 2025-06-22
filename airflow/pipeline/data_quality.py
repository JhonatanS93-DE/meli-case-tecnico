from pipeline.utils import log

def run_quality_checks(df):
    if df is None or df.empty:
        log("[ERROR] El DataFrame está vacío o no fue cargado correctamente.")
        raise ValueError("El DataFrame está vacío.")

    # Chequeo de nulos
    nulls = df.isnull().sum()
    total_nulls = nulls.sum()
    if total_nulls > 0:
        log(f"[WARN] Existen {total_nulls} valores nulos:\n{nulls[nulls > 0]}")
    else:
        log("No hay valores nulos.")

    # Chequeo de duplicados
    duplicated_count = df.duplicated().sum()
    if duplicated_count > 0:
        log(f"[WARN] Existen {duplicated_count} registros duplicados.")
    else:
        log("No hay registros duplicados.")

    # Verificación mínima de columnas clave
    expected_columns = {"user_id", "value_prop_id", "timestamp"}
    missing = expected_columns - set(df.columns)
    if missing:
        log(f"[ERROR] Faltan columnas esperadas: {missing}")
        raise ValueError(f"Faltan columnas requeridas: {missing}")
    else:
        log("Todas las columnas clave están presentes.")
