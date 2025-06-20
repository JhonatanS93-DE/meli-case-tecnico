CREATE TABLE IF NOT EXISTS value_prop_dataset (
    user_id TEXT,
    value_prop_id TEXT,
    timestamp TIMESTAMP,
    was_clicked BOOLEAN,
    views_last_3_weeks INT,
    clicks_last_3_weeks INT,
    payments_last_3_weeks INT,
    total_amount_last_3_weeks FLOAT
);