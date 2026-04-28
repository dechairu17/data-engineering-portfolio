from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import fungsi dari file yang sudah kamu buat sebelumnya
# Pastikan nama file dan fungsi sesuai dengan yang ada di folder modules
from modules.extract_osm import fetch_osm_data
from modules.transform_osm import transform_geospatial_data
from modules.load_to_postgis import load_data_to_postgis

# 1. Definisi Argument Default
# Kegunaan: Mengatur kebijakan retry jika terjadi kegagalan (misal: API Down)
default_args = {
    'owner': 'dimas',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Inisialisasi DAG
# Kegunaan Kode Konfigurasi: schedule_interval='@daily' artinya pipeline ini 
# akan otomatis menarik data Puskesmas baru setiap hari.
with DAG(
    'etl_geospatial_surabaya',
    default_args=default_args,
    description='Pipeline ETL Geospatial untuk Fasilitas Kesehatan Surabaya',
    schedule_interval='@daily', 
    catchup=False
) as dag:

    # 3. Definisi Tugas (Tasks)
    # Kegunaan saat melakukan hal ini: Memisahkan proses menjadi modul-modul kecil 
    # agar jika gagal di tengah (misal: saat Loading), kita tidak perlu mengulang Extraction.
    
    extract_task = PythonOperator(
        task_id='extract_from_osm',
        python_callable=fetch_osm_data
    )

    transform_task = PythonOperator(
        task_id='transform_to_geojson_and_shp',
        python_callable=transform_geospatial_data
    )

    load_task = PythonOperator(
        task_id='load_to_postgis_database',
        python_callable=load_data_to_postgis
    )

    # 4. Alur Kerja (Orchestration)
    # Kegunaan: Menetapkan urutan eksekusi (Dependencies)
    extract_task >> transform_task >> load_task