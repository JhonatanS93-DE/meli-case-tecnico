-- Verifica si la tabla se creó correctamente y sus columnas
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'value_prop_dataset';
SELECT * FROM value_prop_dataset;

-- Conteo total de registros
SELECT COUNT(*) AS total_rows
FROM value_prop_dataset;

-- Top 5 usuarios con más registros
SELECT user_id, COUNT(*) AS total_prints
FROM value_prop_dataset
GROUP BY user_id
ORDER BY total_prints DESC
LIMIT 5;

-- Importe total gastado por value prop
SELECT value_prop_id, SUM(total_amount_last_3_weeks) AS total_spent
FROM value_prop_dataset
GROUP BY value_prop_id
ORDER BY total_spent DESC;