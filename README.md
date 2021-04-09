# From Keras to Production

## OUTDATED! FOR THE NEWEST VERSION SEE https://github.com/codecentric/from-jupyter-to-production-workshop (a fork of this repository)


## Data Source

https://www.kaggle.com/moltean/fruits

## Notebooks

https://github.com/codecentric/from-keras-to-production-workshop.git

## Used Docker Images
```bash
docker pull codecentric/from-keras-to-production-baseimage
docker pull codecentric/tensorflow-serving-baseimage
docker pull tsabsch/airflow-baseimage
```

## Start Jupyterlab
### With docker-compose (recommended, no Docker Toolbox)
```bash
# Without Airflow
docker-compose up

# With Airflow
docker-compose -f docker-compose.yml -f optional-airflow.yml up
```

### Without docker-compose
#### Jupyterlab
```bash
# Linux/Mac (Docker version >= 17.06)
docker run -p 8888:8888 --mount type=bind,source=$(pwd)/notebooks,target=/keras2production/notebooks codecentric/from-keras-to-production-baseimage

# Docker for Windows (Docker version >= 17.06)
docker run -p 8888:8888 --mount type=bind,source=%cd%/notebooks,target=/keras2production/notebooks codecentric/from-keras-to-production-baseimage

# Docker for Windows (Docker version < 17.06)
docker run -p 8888:8888 -v %cd%/notebooks:/keras2production/notebooks codecentric/from-keras-to-production-baseimage

# Docker Toolbox (Windows 7, 8 and Windows 10 Home; a separate VM for Docker)
docker run -d -p 8888:8888 codecentric/from-keras-to-production-baseimage
# Copy notebooks manually into the container
## get container id
docker ps
## copy into container
docker cp notebooks <container id>:/keras2production
# After the first day, stop the container
docker stop <container id>
# On the second day, start the container again
docker start <container id>
```

With Docker Toolbox, the JupyterLab instance might be available at `192.168.99.100:8888`, not `localhost:8888`.

#### TensorFlow Serving
```bash
docker run -p 8501:8501 -p 8500:8500 --mount type=bind,source=$(pwd)/notebooks/12-models/fruits/,target=/models/fruits -e MODEL_NAME=fruits codecentric/tensorflow-serving-baseimage
```

#### Airflow
```bash
# Docker for Linux/Mac/Windows (Docker Version >= 17.06)
docker run -p 8080:8080 --mount type=bind,source=$(pwd)/notebooks/04-airflow/dags,target=/usr/local/airflow/dags \
                        --mount type=bind,source=$(pwd)/notebooks/04-airflow/exercise-dataset,target=/exercise-dataset \
                        tsabsch/airflow-baseimage

# Docker for Windows (Docker version < 17.06)
docker run -p 8080:8080 -v %cd%/notebooks/04-airflow/dags:/usr/local/airflow/dags \
                        -v %cd%/notebooks/04-airflow/exercise-dataset:/exercise-dataset \
                        tsabsch/airflow-baseimage

# Docker Toolbox (Windows 7, 8 and Windows 10 Home)
docker run -d -p 8080:8080 tsabsch/airflow-baseimage
# Copy notebooks manually into the container
## get container
docker ps
## copy into container
docker cp notebooks/04-airflow/exercise-dataset <container id>:/exercise-dataset
docker cp notebooks/04-airflow/dags <container id>:/usr/local/airflow/dags
```

#### In general 
- Replace current directory in commands with either `%cd%` (Windows) or `$(pwd)` Mac/Linux
- `--mount` is supported since Docker version 17.06. If you use an older version you have to use `-v` (Volumes). See the Example in the Airflow section above.

## Old Slides
```bash
pip install -r requirements.txt
cd slides
jupyter nbconvert end2end_ds.ipynb --to slides --post serve --reveal-prefix=reveal.js
```

## References and Further Information

#### General

- [Cheatsheet for working with IPython/Jupyter](https://ipython.readthedocs.io/en/stable/interactive/python-ipython-diff.html)

- [Cheatsheet for Docker](https://hackernoon.com/docker-commands-the-ultimate-cheat-sheet-994ac78e2888)

- [Free notebooks from the book "Deep Learning with Python"](https://github.com/fchollet/deep-learning-with-python-notebooks)

- [Introduction to Reinforcement Learning (Youtube)](https://www.youtube.com/watch?v=FCyZplb0ul4)

- [Keras examples](https://github.com/keras-team/keras/tree/master/examples)

#### Convolutional Networks

- [Visualization of image kernels](http://setosa.io/ev/image-kernels/)

- [Visualization of activation maps](https://jacobgil.github.io/deeplearning/class-activation-maps)

- [Combining channels in convolutional layers](https://towardsdatascience.com/intuitively-understanding-convolutions-for-deep-learning-1f6f42faee1)

#### Natural Language Processing

- [Using pre-trained word embeddings in a Keras model](https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html)

- [Text preprocessing](https://keras.io/preprocessing/text)

#### Production-Ready Data Science

- [What’s your ML test score? A rubric for ML production systems](https://ai.google/research/pubs/pub45742)

- [A walkthrough of DVC](https://blog.codecentric.de/en/2019/03/walkthrough-dvc/),
  [DVC dependency management](https://blog.codecentric.de/en/2019/08/dvc-dependency-management/)
