import os
import tensorflow as tf
from tensorflow import keras
from . import config


def load_model():
    path = config.MODEL_PATH
    model = None
    trained = False
    if path and os.path.exists(path):
        try:
            model = tf.keras.models.load_model(path)
            trained = True
            print("Model loaded:", path)
        except Exception as e:
            print("Model load failed:", e)
    else:
        print("Model file not found:", path)
    if model is not None:
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])
    return model, trained