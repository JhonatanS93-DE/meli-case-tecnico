def run_quality_checks(df):
    """Run simple quality checks to validate data integrity"""
    assert df is not None, "DataFrame is None"
    assert not df.empty, "DataFrame is empty"
    assert "user_id" in df.columns, "Missing user_id"
    assert "value_prop_id" in df.columns, "Missing value_prop_id"
    print("✔ Passed data quality checks")
