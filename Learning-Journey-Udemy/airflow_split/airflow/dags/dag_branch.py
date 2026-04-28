from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.utils.dates import datetime

def pilih_cabang():
    hari_ini = datetime.today().weekday()
    if hari_ini < 6:
        return 'task_hari_kerja'
    else:
        return 'task_weekend'

with DAG(
    dag_id='dag_branching',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    cabang = BranchPythonOperator(
        task_id='pilih_cabang',
        python_callable=pilih_cabang
    )

    task_kerja = PythonOperator(
        task_id='task_hari_kerja',
        python_callable=lambda: print("Ini hari kerja")
    )

    task_libur = PythonOperator(
        task_id='task_weekend',
        python_callable=lambda: print("Ini akhir pekan")
    )

    cabang >> [task_kerja, task_libur]
