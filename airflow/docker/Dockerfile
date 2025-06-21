FROM apache/airflow:2.7.1

COPY requirements.txt /requirements.txt

USER root
RUN pip install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

USER airflow
