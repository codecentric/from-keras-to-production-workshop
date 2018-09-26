# data2day-workshop

## Daten

https://www.kaggle.com/moltean/fruits

## Images pullen
- docker pull codecentric/from-keras-to-production-baseimage
- docker pull codecentric/tensorflow-serving-baseimage

## Jupyterlab starten
```bash
docker run -p 8888:8888 -v $(pwd)/notebooks:/keras2production/notebooks codecentric/from-keras-to-production-baseimage
```
## TensorFlow Serving starten
docker run -p 8501:8501 -p 8500:8500 --mount type=bind,source=$(pwd)/notebooks/6-models/fruits/,target=/models/fruits -e MODEL_NAME=fruits -t tensorflow/serving:1.10.1

## Run slides
```bash
pip install -r requirements.txt
cd slides
jupyter nbconvert end2end_ds.ipynb --to slides --post serve --reveal-prefix=reveal.js
```
