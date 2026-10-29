import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from porang.app import app  # noqa: E402

if __name__ == "__main__":
    from porang import config

    app.run(host="0.0.0.0", port=config.PORT, debug=True)