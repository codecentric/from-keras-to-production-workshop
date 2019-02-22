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


def configure(outpath):
    generator = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)
    with open(outpath, "wb") as f:
        pickle.dump(generator, f)
        
        
def build_generator(config_path, 
                    dataset_path, 
                    data_set_type,
                    img_height=100, img_width=100):
    with open(config_path, "rb") as f:
        generator = pickle.load(f)
    path = "%s/%s" % (dataset_path, data_set_type)
    return generator.flow_from_directory(path,
                                         target_size=(img_height, 
                                                      img_width),
                                         color_mode='rgb')


def define_model(input_shape, num_classes):
    model = keras.models.Sequential()
    model.add(
    keras.layers.Conv2D(filters=4, kernel_size=(2, 2), strides=1, activation='relu', input_shape=input_shape))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Conv2D(filters=4, kernel_size=(2, 2), strides=1, activation='relu'))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(rate=0.25))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=8, activation='relu'))
    model.add(keras.layers.Dropout(rate=0.5))
    model.add(keras.layers.Dense(units=num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    return model
    

def train_model(dataset_path, config_path, out_path, training_set="Training", epochs=2):
    dataset = dataset_path
    config = config_path
    training_data = build_generator(config, dataset, training_set)
    input_shape = training_data.image_shape
    num_classes = len(training_data.class_indices)
    model = define_model(input_shape, num_classes)
    steps_per_epoch = training_data.samples // training_data.batch_size
    model.fit_generator(training_data,
                        steps_per_epoch=steps_per_epoch,
                        epochs=epochs,
                        verbose=0)
    model.save(out_path)
        
        
def export(model_path, out_path):
    model_path = model_path
    model = keras.models.load_model(model_path)
    tensor_info_input = tf.saved_model.utils.build_tensor_info(model.input)
    tensor_info_output = tf.saved_model.utils.build_tensor_info(model.output)
    prediction_signature = (
        tf.saved_model.signature_def_utils.build_signature_def(
            inputs={'input': tensor_info_input},
            outputs={'prediction': tensor_info_output},
            method_name=signature_constants.PREDICT_METHOD_NAME))

    export_path = out_path
    tf_builder = builder.SavedModelBuilder(export_path)
    with keras.backend.get_session() as sess:
        tf_builder.add_meta_graph_and_variables(
            sess=sess,
            tags=[tag_constants.SERVING],
            signature_def_map={
                signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature
            }
        )
    tf_builder.save()
    
        
if __name__ == '__main__':
  fire.Fire()