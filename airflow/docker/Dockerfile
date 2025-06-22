FROM apache/airflow:2.7.1

COPY ./airflow/docker/requirements.txt /requirements.txt

USER root
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./airflow/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER airflow
ENTRYPOINT ["/entrypoint.sh"]
