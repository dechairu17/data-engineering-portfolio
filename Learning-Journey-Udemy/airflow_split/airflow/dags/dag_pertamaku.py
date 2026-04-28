from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator 

# 1. Default Arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 2. Buat Objek DAG terlebih dahulu
dag = DAG(
    dag_id='dag_pertama_v03',
    default_args=default_args,
    description='DAG pertama untuk latihan',
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['latihan']
)

# 3. Definisikan fungsi Python
def halo():
    print("Halo dari DAG!")

# 4. Definisikan Task dengan parameter `dag=dag`
task1 = PythonOperator(
    task_id='cetak_hello_task',
    python_callable=halo,
    dag=dag  # Menyisipkan DAG sebagai parameter
)

task2 = BashOperator(
    task_id='bash_halo_task_1',
    bash_command='echo "halo dari bash operator 1"',
    dag=dag
)

task3 = BashOperator(
    task_id='bash_halo_task_2',
    bash_command='echo "halo dari bash operator 2"',
    dag=dag
)

# Mendefinisikan task dependency dimana task2 berjalan setelah task1
# task1 >> task2 >> task3

task1 >> [task2, task3]

# task2.set_upstream(task1)  # task1 harus selesai dulu
# task2.set_downstream(task3)  # task3 menunggu task2