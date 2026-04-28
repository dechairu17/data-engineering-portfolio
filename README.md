# Data Engineering Portfolio 🚀

Selamat datang di repositori portofolio saya. Repositori ini merangkum proyek teknis dan perjalanan belajar saya sebagai mahasiswa **Teknik Informatika Polinema**.

---

## 🏆 Featured Project: Surabaya Geospatial ETL Pipeline
Pipeline otomatis untuk mengambil data fasilitas kesehatan Surabaya dari OpenStreetMap dan menyimpannya ke database PostGIS.

### 🏗️ Arsitektur Pipeline
```mermaid
graph LR
    A[OpenStreetMap API] -->|Extract: Python| B(Raw Data: JSON)
    B -->|Transform: GeoPandas| C(Processed: GeoJSON)
    C -->|Load: SQLAlchemy| D[(PostGIS Database)]
    
    subgraph Orchestration
    E[Apache Airflow] -.-> A
    E -.-> B
    E -.-> C
    E -.-> D
    end
