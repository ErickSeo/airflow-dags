from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3
import time

EMR_APPLICATION_ID = "YOUR_APPLICATION_ID"
EMR_ROLE_ARN = "arn:aws:iam::123456789012:role/EMRServerlessJobRole"

def submit_emr_job(**context):
    client = boto3.client("emr-serverless", region_name="us-east-1")
    
    response = client.start_job_run(
        applicationId=EMR_APPLICATION_ID,
        executionRoleArn=EMR_ROLE_ARN,
        jobDriver={
            "sparkSubmit": {
                "entryPoint": "s3://meu-bucket/code/process.py",
                "entryPointArguments": ["arg1", "arg2"],
                "sparkSubmitParameters": "--conf spark.executor.memory=4g"
            }
        },
        configurationOverrides={
            "monitoringConfiguration": {
                "s3MonitoringConfiguration": {
                    "logUri": "s3://meu-bucket/logs/"
                }
            }
        }
    )

    job_run_id = response["jobRunId"]
    context['ti'].xcom_push(key="emr_job_run_id", value=job_run_id)
    print(f"Job submitted: {job_run_id}")


def wait_for_emr_job(**context):
    client = boto3.client("emr-serverless", region_name="us-east-1")
    job_run_id = context['ti'].xcom_pull(task_ids='submit_emr_job', key='emr_job_run_id')

    while True:
        response = client.get_job_run(
            applicationId=EMR_APPLICATION_ID,
            jobRunId=job_run_id
        )
        state = response['jobRun']['state']
        print(f"Job status: {state}")

        if state in ["SUCCESS", "FAILED", "CANCELLED"]:
            if state != "SUCCESS":
                raise Exception(f"EMR job failed with state: {state}")
            break
        time.sleep(30)


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="emr_serverless_job_dag",
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["emr", "aws"]
) as dag:

    submit = PythonOperator(
        task_id="submit_emr_job",
        python_callable=submit_emr_job,
        provide_context=True
    )

    wait = PythonOperator(
        task_id="wait_for_emr_job",
        python_callable=wait_for_emr_job,
        provide_context=True
    )

    submit >> wait