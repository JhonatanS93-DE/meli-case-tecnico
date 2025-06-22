FROM apache/airflow:2.7.1

COPY ./airflow/docker/requirements.txt /requirements.txt

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"
