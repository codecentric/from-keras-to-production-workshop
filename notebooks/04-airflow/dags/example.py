import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='example',
    default_args=default_args,
    schedule_interval=None,
)


def print_sth():
    print("Hello World.")


task1= PythonOperator(
    task_id="print",
    python_callable=print_sth,
    dag=dag,
)


def do_some_math(x, y):
    print(x + y)

             
task2 = PythonOperator(
    task_id="math",
    python_callable=do_some_math,
    op_args=[1,2],
    dag=dag,
)


task1 >> task2
