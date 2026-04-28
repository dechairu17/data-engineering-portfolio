import geopandas as gpd
from sqlalchemy import create_engine, text
import datetime
import os

def load_data_to_postgis():
    # 1. Path Dinamis
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_geojson = os.path.join(current_dir, '..', 'health_facilities.geojson')

    # 2. Koneksi ke Database 'airflow' di kontainer 'postgis'
    engine = create_engine('postgresql://airflow:airflow@postgis:5432/airflow')

    if not os.path.exists(input_geojson):
        raise FileNotFoundError(f"File tidak ditemukan: {input_geojson}")

    print(f"Membaca data: {input_geojson}")
    gdf = gpd.read_file(input_geojson)

    # 3. Proses Loading ke PostGIS
    print("Memasukkan data ke tabel health_facilities...")
    try:
        gdf.to_postgis(
            name='health_facilities', 
            con=engine, 
            if_exists='replace', 
            index=False
        )

        # 4. Update Metadata dengan engine.begin() (Otomatis Commit)
        print("Memperbarui metadata...")
        with engine.begin() as conn:
            # Pastikan tabel metadata ada
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS data_inventory_metadata (
                    table_name TEXT PRIMARY KEY,
                    last_updated TIMESTAMP
                );
            """))
            
            # Upsert (Insert atau Update jika konflik)
            conn.execute(text("""
                INSERT INTO data_inventory_metadata (table_name, last_updated)
                VALUES ('health_facilities', :now)
                ON CONFLICT (table_name) DO UPDATE SET last_updated = EXCLUDED.last_updated;
            """), {"now": datetime.datetime.now()})

        print(f"BERHASIL! {len(gdf)} data masuk ke PostGIS.")

    except Exception as e:
        print(f"GAGAL saat loading: {e}")
        raise e 

if __name__ == "__main__":
    load_data_to_postgis()