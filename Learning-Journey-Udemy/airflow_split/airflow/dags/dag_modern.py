from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False)
def dag_decorator():
    
    @task
    def extract():
        return [1, 2, 3]
    
    @task
    def transform(data):
        return [x * 2 for x in data]
    
    @task
    def load(data):
        print(f"Loaded data: {data}")
    
    data = extract()
    transformed = transform(data)
    load(transformed)

etl_dag = dag_decorator()