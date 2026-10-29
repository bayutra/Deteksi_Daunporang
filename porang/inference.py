import os
import numpy as np
import cv2
from . import config


def preprocess_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Cannot read image: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, config.IMAGE_SIZE)
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, 0)


def predict(model, img_path):
    img = preprocess_image(img_path)
    preds = model.predict(img, verbose=0)[0]
    idx = int(np.argmax(preds))
    return {
        "disease": config.CLASS_NAMES[idx],
        "confidence": round(float(preds[idx]) * 100, 1),
        "all": {config.CLASS_NAMES[i]: round(float(preds[i]) * 100, 1)
                for i in range(len(config.CLASS_NAMES))},
    }