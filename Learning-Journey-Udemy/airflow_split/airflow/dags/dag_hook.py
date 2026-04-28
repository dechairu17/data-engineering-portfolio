from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime

def fetch_data_postgres():
    hook = PostgresHook(postgres_conn_id='postgres_con')
    conn = hook.get_conn() # Mendapatkan koneksi langsung ke database PostgreSQL melalui hook.
    cursor = conn.cursor() # Membuat objek cursor dari koneksi PostgreSQL untuk mengeksekusi perintah SQL.
    cursor.execute("SELECT * FROM karyawan") # Menjalankan query SQL untuk mengambil semua data dari tabel karyawan.
    records = cursor.fetchall() # Mengambil semua hasil dari query dan menyimpannya dalam variabel records.
    for row in records: 
        print(row)

with DAG(
    dag_id='dag_hook',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["example", "postgres"]
) as dag:
    
    task_hook = PythonOperator(
        task_id='fetch_users_from_postgres',
        python_callable=fetch_data_postgres
    )

    task_hook