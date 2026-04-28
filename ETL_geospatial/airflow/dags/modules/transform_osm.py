import pandas as pd
import geopandas as gpd
import json
import os

def transform_geospatial_data():
    # 1. Tentukan Path secara Dinamis
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, '..', 'raw_health_facilities.json')
    output_geojson = os.path.join(current_dir, '..', 'health_facilities.geojson')
    output_shp = os.path.join(current_dir, '..', 'health_facilities.shp')

    # 2. Load Data
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Data mentah tidak ditemukan di: {input_file}")

    with open(input_file, 'r') as f:
        raw_data = json.load(f)

    # ... (Proses ekstraksi records tetap sama) ...
    records = []
    for el in raw_data.get('elements', []):
        if el.get('type') == 'node':
            records.append({
                'id': el.get('id'),
                'lat': el.get('lat'),
                'lon': el.get('lon'),
                'name': el.get('tags', {}).get('name', 'Tanpa Nama'),
                'type': el.get('tags', {}).get('amenity')
            })

    df = pd.DataFrame(records)
    df = df.dropna(subset=['lat', 'lon'])
    df = df[(df['lat'] < 0) & (df['lon'] > 110)] 

    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.lon, df.lat),
        crs="EPSG:4326"
    )

    # 3. Export menggunakan path dinamis
    gdf.to_file(output_geojson, driver='GeoJSON', engine='pyogrio')
    gdf.to_file(output_shp, engine='pyogrio')

    print(f"Transformasi selesai! File disimpan di folder dags.")