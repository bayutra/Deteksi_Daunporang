import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

IMAGE_SIZE = (224, 224)
NUM_CLASSES = 3

# Single model (EfficientNetB0 baseline)
_MODEL_CANDIDATES = ["baseline_porang.keras", "efficientnet_porang.keras",
                     "model_porang.keras"]
MODEL_PATH = None
for c in _MODEL_CANDIDATES:
    p = os.path.join(MODELS_DIR, c)
    if os.path.exists(p):
        MODEL_PATH = p
        break
if os.getenv("MODEL_PATH"):
    MODEL_PATH = os.getenv("MODEL_PATH")
if MODEL_PATH is None:
    MODEL_PATH = os.path.join(MODELS_DIR, "baseline_porang.keras")

CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

CLASS_NAMES = ["DAUN SEHAT", "HAWAR DAUN", "KARAT BERCAK"]
if os.path.exists(CLASS_INDICES_PATH):
    try:
        with open(CLASS_INDICES_PATH) as f:
            ci = json.load(f)
        inv = {v: k for k, v in ci.items()}
        CLASS_NAMES = [str(inv[i]) for i in range(len(inv))]
    except Exception:
        pass

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
PORT = int(os.getenv("PORT", "5000"))
MODEL_NAME = "EfficientNetB0"

# Guard porang-only
MIN_LEAF_GREEN_FRACTION = float(os.getenv("MIN_LEAF_GREEN_FRACTION", "0.08"))
MIN_LEAF_REGION_FRACTION = float(os.getenv("MIN_LEAF_REGION_FRACTION", "0.04"))
MIN_PREDICTION_CONFIDENCE = float(os.getenv("MIN_PREDICTION_CONFIDENCE", "60.0"))