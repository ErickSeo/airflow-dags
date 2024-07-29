from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

default_args={
   'depends_on_past': False,
   'email': ['abcd@gmail.com'],
   'email_on_failure': False,
   'email_on_retry': False,
   'retries': 1,
   'retry_delay': timedelta(minutes=5)
}
with DAG(
   'trip-analytics-dag',
   default_args=default_args,
   description='analytics dag',
   schedule_interval=timedelta(days=1),
   start_date=datetime(2022, 11, 17),
   catchup=False,
   tags=['example']
) as dag:
   t1 = SparkKubernetesOperator(
       task_id='analytics',
       trigger_rule="all_success",
       depends_on_past=False,
       retries=3,
       application_file="manifest.yaml",
       namespace="processing",
       in_cluster=True,
       api_group="sparkoperator.k8s.io",
       api_version="v1beta2",
       do_xcom_push=True,
       dag=dag
   )
