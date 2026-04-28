from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.filesystem import FileSensor

# 1. Default Arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 2. Buat Objek DAG terlebih dahulu
dag = DAG(
    dag_id='dag_sensor',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['latihan']
)

task_menunggu_file = FileSensor(
    task_id='tunggu_file_init',
    filepath='init.sql',
    poke_interval=10,
    timeout=500,
    mode='poke',
    dag=dag
)

# 3. Membuat task dengan menggunakan postgres operator
task_membuat_tabel = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_con',
    sql='./files/init.sql',
    dag=dag,
)

# 4. Menjalankan task
task_menunggu_file >> task_membuat_tabel