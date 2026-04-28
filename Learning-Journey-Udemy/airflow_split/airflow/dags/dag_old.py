from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    return [1, 2, 3]

def transform(ti):  # menggunakan XCom
    data = ti.xcom_pull(task_ids='extract')
    return [x * 2 for x in data]

def load(ti):
    data = ti.xcom_pull(task_ids='transform')
    print(f"Loaded data: {data}")

with DAG(
    dag_id='dag_traditional',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    task_load = PythonOperator(
        task_id='load',
        python_callable=load
    )

    task_extract >> task_transform >> task_load