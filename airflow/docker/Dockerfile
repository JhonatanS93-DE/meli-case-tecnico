FROM apache/airflow:2.7.1

COPY ./airflow/docker/requirements.txt /requirements.txt
COPY ./airflow/docker/entrypoint.sh /entrypoint.sh

USER root
RUN pip install --no-cache-dir -r /requirements.txt
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

USER airflow
ENTRYPOINT ["/entrypoint.sh"]
