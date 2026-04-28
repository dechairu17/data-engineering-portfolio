from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime

def gagal():
    raise ValueError("Sengaja gagal")

def sukses():
    print("Berhasil bro!")

def follow_up():
    print("Semua task sebelumnya gagal. Jalan sekarang.")

with DAG(
    dag_id='dag_trigger_rule_v02',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='task_1',
        python_callable=gagal
    )

    task2 = PythonOperator(
        task_id='task_2',
        python_callable=gagal
    )

    task_gagal_semua = PythonOperator(
        task_id='tindak_lanjut_kegagalan',
        python_callable=follow_up,
        trigger_rule='all_failed'  # atau bisa pakai string: 'all_failed'
    )

    [task1, task2] >> task_gagal_semua
