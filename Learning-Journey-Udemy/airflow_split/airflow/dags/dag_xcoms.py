from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def push_data(ti):
    ti.xcom_push(key='data_xcoms', value='Halo dari Task A')

def pull_data(ti):
    data = ti.xcom_pull(task_ids='task_a', key='data_xcoms')
    print(f'Data diterima: {data}')

with DAG(
    dag_id='dag_xcoms',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=push_data,
    )

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=pull_data,
    )

    task_a >> task_b