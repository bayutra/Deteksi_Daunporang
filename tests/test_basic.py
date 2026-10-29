import os
import tempfile
import numpy as np
from PIL import Image

from porang import config
from porang.inference import preprocess_image


def test_preprocess_shape():
    # create a temp image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img = Image.new("RGB", (100, 100), color=(10, 20, 30))
        img.save(f.name)
        path = f.name
    try:
        arr = preprocess_image(path)
        assert arr.shape == (1, 224, 224, 3)
        assert arr.dtype == np.float32
        assert arr.min() >= 0 and arr.max() <= 1
    finally:
        os.remove(path)


def test_config_classes():
    assert len(config.CLASS_NAMES) == 3


def test_health_endpoint():
    # import app (model may load)
    import app as appmod
    client = appmod.app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"