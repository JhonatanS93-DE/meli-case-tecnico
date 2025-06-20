# Mercado Libre - Senior Data Engineer Case

## 📝 Descripción del Caso

Este proyecto corresponde a la resolución de un ejercicio técnico para la posición de **Senior Data Engineer** en Mercado Libre. El objetivo es construir un pipeline de datos que procese múltiples fuentes, genere un dataset enriquecido para un modelo de machine learning y lo almacene en diferentes formatos y destinos.

---

## 🚀 Objetivos del Pipeline

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

## 🛠️ Tecnologías y Herramientas

- **Python 3.10+**
- **Apache Airflow** (vía Docker Compose)
- **PostgreSQL** (DBeaver como cliente de consulta)
- **Pandas / PyArrow**
- **Docker + Docker Compose**

---

## 📂 Estructura del Proyecto

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

## ⚙️ Cómo Ejecutar el Proyecto

1. Clona este repositorio:
```bash
git clone https://github.com/JhonatanS93-DE/meli-case-tecnico.git
cd meli-case-tecnico
```

2. Asegúrate de tener instalado `Docker` y `Docker Compose`.

3. Ejecuta el entorno:
```bash
docker-compose up --build
```

4. Accede a Airflow:
```
http://localhost:8080
(user: admin / password: admin)
```

5. Sube tus archivos fuente a `data/input/` y ejecuta el DAG `mercado_libre_pipeline_dag`.

---

## ✅ Mejoras Futuras

- Tests automatizados con `pytest`.
- Validaciones de esquema con `Great Expectations`.
- Parametrización por entorno.
- Orquestación con DAGs más robustos y modularización por etapa.

---

## 🧑‍💻 Autor

**Jhonatan Saldarriaga**  
[LinkedIn](https://www.linkedin.com/in/jhonatan-saldarriaga/)  
Senior Data Engineer