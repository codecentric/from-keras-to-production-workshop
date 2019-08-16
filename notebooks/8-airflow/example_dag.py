import time
from pprint import pprint
from datetime import datetime

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='my_dag',
    default_args=default_args,
    schedule_interval=None,
)

today = datetime.today().strftime("%m-%d-%Y")
input_img = f"exercise-dataset/daily/{today}/image.jpg"
preproc_img = f"exercise-dataset/daily/{today}/preprocessed.jpg"
prediction = f"exercise-dataset/daily/{today}/result.json"

file_sensor = FileSensor(
    task_id="wait_data_exists",
    filepath=input_img,
    dag=dag
)

def preprocess_img():
    img = cv2.imread(input_img, cv2.IMREAD_COLOR)
    larger = cv2.resize(img, (100,100))
    gray = cv2.cvtColor(larger, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_img, gray)

preprocess = PythonOperator(
    task_id='preprocess',
    python_callable=preprocess_img,
    dag=dag,
)


def predict_img():
    img = cv2.imread(self.input().path, cv2.IMREAD_GRAYSCALE)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp=2, 
        minDist=15, param1=100, param2=70
    )
    label = "lemon" if circles is not None else "banana"
    with open(prediction, "w") as out:
        json.dump({"class": label}, out)

predict = PythonOperator(
    task_id='predict',
    python_callable=predict_img,
    dag=dag,
)

notify = EmailOperator(
    task_id='notify',
    to='tim.sabsch@codecentric.de',
    subject='Your daily prediction has finished!',
    html_content='Gratz!',
    dag=dag,
)

# connect our pipeline steps
file_sensor >> preprocess >> predict >> notify