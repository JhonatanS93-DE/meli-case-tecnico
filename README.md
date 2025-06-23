# Mercado Libre - Case Tecnico

## Descripción del Caso

Este proyecto corresponde a la resolución de un ejercicio técnico para la posición de **Senior Data Engineer** en Mercado Libre. El objetivo es construir un pipeline de datos que procese múltiples fuentes, genere un dataset enriquecido para un modelo de machine learning y lo almacene en diferentes formatos y destinos.

---

## Objetivos del Pipeline

- Leer fuentes de datos en formato JSONL y CSV (`prints.json`, `taps.json`, `pays.csv`).
- Filtrar eventos de la última semana.
- Calcular métricas agregadas para las tres semanas previas:
  - Número de vistas (`prints`)
  - Número de clics (`taps`)
  - Número y monto de pagos (`pays`)
- Enriquecer los datos con estas métricas.
- Validar la calidad del dataset resultante.
- Guardar el dataset final en:
  - CSV
  - Parquet
  - PostgreSQL

---

## Tecnologías y Herramientas

- **Python 3.10+**
- **Apache Airflow** (vía Docker Compose)
- **PostgreSQL** (DBeaver como cliente de consulta en BD)
- **Pandas**
- **Docker + Docker Compose**

---

## Estructura del Proyecto

```
├── airflow/
│   ├── dags/                # DAG principal de Airflow
│   └── docker/              # Dockerfile y dependencias
├── data/
│   ├── input/               # Archivos fuente
│   └── output/              # Salidas CSV / Parquet
├── notebooks/               # Análisis exploratorio
├── pipeline/                # Código modular de ETL
├── sql/                     # Scripts SQL (creación de tablas)
├── .env                     # Variables de entorno (opcional)
├── docker-compose.yml       # Orquestación de servicios
└── README.md
```

---

## Cómo Ejecutar el Proyecto

1. Clona este repositorio:
```bash
git clone https://github.com/JhonatanS93-DE/meli-case-tecnico.git
cd meli-case-tecnico
```

2. Asegúrate de tener instalado `Docker` y `Docker Compose`.

3. Ejecuta el entorno:
```bash
docker-compose build
docker-compose run airflow airflow db init
docker-compose up
```

4. Accede a Airflow:
```
http://localhost:8080
(user: admin / password: admin)

Si tienes inconvenientes al ingresar por usuario y pass, puedes correr este codigo en bash para asignarlas:

docker-compose exec airflow airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

```

5. Sube tus archivos fuente a `data/input/` y ejecuta el DAG `mercado_libre_pipeline_dag`.
Los resultados se alojaran en la carpeta `data/output`

1-Archivos csv
2-Archivo parquet
3-Base de datos

---

## Analisis Exploratorio

Se realiza analisis exploratorio para explicar en un notebook de `Jupyter Notebook`
con el mismo comando Jupyter Notebook.
El cual puedes ejecutar desde tu terminal y automaticamente se abre la conexion en 
http://localhost:8888

Nota: Para poder ejecutarlo primero debes tener el resultado del dataset_final y acomodar la ruta del archivo.

---

## Mejoras Futuras

- Tests automatizados con `pytest`.
- Validaciones de esquema con `Great Expectations`.
- Aplicar uso de servicios cloud 

---

## Autor

**Jhonatan Saldarriaga**  
[LinkedIn](https://www.linkedin.com/in/jhonatan-saldarriaga/)  
Senior Data Engineer
