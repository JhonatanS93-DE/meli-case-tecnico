from pipeline.utils import log

def run_quality_checks(df):
    assert df is not None, "DataFrame is None"
    assert not df.empty, "DataFrame is empty"
    assert "user_id" in df.columns, "Falta columna user_id"
    assert "value_prop_id" in df.columns, "Falta columna value_prop_id"
    assert df["was_clicked"].isin([True, False]).all(), "Valores inválidos en was_clicked"
    log("✔ Validación de calidad de datos completada.")