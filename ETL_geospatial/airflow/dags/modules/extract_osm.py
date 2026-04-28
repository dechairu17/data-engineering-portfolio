import requests
import json
import os

def fetch_osm_data():
    url = "https://overpass-api.de/api/interpreter"
    
    # 1. Tentukan Path secara Dinamis
    # Mengambil folder tempat script ini berada (modules) lalu naik satu level ke folder 'dags'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'raw_health_facilities.json')
    
    query = """
    [out:json][timeout:25];
    (
      node["amenity"="clinic"](-7.36, 112.59, -7.17, 112.83);
      node["amenity"="hospital"](-7.36, 112.59, -7.17, 112.83);
    );
    out body;
    """
    
    headers = {
        'User-Agent': 'GeospatialETLProject/1.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    print(f"Sedang mengambil data dari OpenStreetMap...")
    
    try:
        response = requests.post(url, data={'data': query}, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Menulis file menggunakan path absolut yang sudah didapat
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"Berhasil! Tersimpan di: {file_path}")
            return True # Beri sinyal sukses untuk Airflow
        else:
            raise Exception(f"API Error: {response.status_code} - {response.reason}")
            
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        raise e # Melempar error agar Airflow mencatat 'FAILED' dengan jelas