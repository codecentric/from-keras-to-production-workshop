import sys, os
import keras
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import builder

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
    print("saved")
    

if __name__ == '__main__':
    model = sys.argv[1]
    print(model)
    out = sys.argv[2]
    print(out)
    export(model, out)
    print("after")