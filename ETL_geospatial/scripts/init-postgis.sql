CREATE DATABASE geospatial_db;
-- Masuk ke database geospatial_db
\c geospatial_db;

-- 1. Aktifkan PostGIS
-- Kegunaan: Mengaktifkan fungsi spasial (seperti menghitung jarak) di database ini.
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Buat Tabel Utama dengan kolom GEOMETRY
-- Kegunaan Kode: Tipe GEOMETRY(Point, 4326) memastikan hanya data titik WGS84 yang bisa masuk.
CREATE TABLE IF NOT EXISTS health_facilities (
    id SERIAL PRIMARY KEY,
    osm_id BIGINT,
    name TEXT,
    amenity_type TEXT,
    geom GEOMETRY(Point, 4326)
);

-- 3. Buat Tabel Metadata
-- Kegunaan saat melakukan hal ini: Sesuai standar pemerintah (SDI), 
-- setiap data harus punya catatan sumber dan tanggal agar bisa dipertanggungjawabkan.
CREATE TABLE IF NOT EXISTS data_inventory_metadata (
    table_name TEXT PRIMARY KEY,
    source_api TEXT,
    last_updated TIMESTAMP,
    epsg_code INTEGER,
    description TEXT
);

-- Catat metadata awal
INSERT INTO data_inventory_metadata (table_name, source_api, last_updated, epsg_code, description)
VALUES ('health_facilities', 'OpenStreetMap Overpass API', CURRENT_TIMESTAMP, 4326, 'Data Puskesmas dan RS Surabaya')
ON CONFLICT (table_name) DO UPDATE SET last_updated = EXCLUDED.last_updated;