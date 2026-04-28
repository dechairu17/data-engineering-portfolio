from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

# 1. Default Arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 2. Buat Objek DAG terlebih dahulu
dag = DAG(
    dag_id='dag_postgres',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['latihan']
)

# 3. Membuat task dengan menggunakan postgres operator
task_membuat_tabel = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_con',
    sql="""
			CREATE TABLE IF NOT EXISTS karyawan (
			    id SERIAL PRIMARY KEY,
			    nama TEXT NOT NULL,
			    tanggal_lahir DATE NOT NULL
			);
			
			INSERT INTO karyawan (nama, tanggal_lahir) VALUES
			('Andi Saputra', '1990-03-15'),
			('Budi Santoso', '1988-07-22'),
			('Citra Lestari', '1992-11-30'),
			('Dewi Anggraini', '1985-01-10'),
			('Eko Prasetyo', '1995-05-05'),
			('Fajar Nugroho', '1993-12-01'),
			('Gita Permata', '1989-08-19'),
			('Hendra Wijaya', '1991-02-14'),
			('Intan Maharani', '1994-06-25'),
			('Joko Susilo', '1987-09-09');
    """,
    dag=dag,
)

# 4. Menjalankan task
task_membuat_tabel