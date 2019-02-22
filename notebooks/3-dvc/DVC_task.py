import fire
import json
import keras
from keras.models import load_model
import pickle
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import builder
import os

    
        
if __name__ == '__main__':
  fire.Fire()