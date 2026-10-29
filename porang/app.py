import logging
import os
import uuid
from datetime import datetime

from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from . import config
from .analysis import analyze_image, is_porang_leaf
from .db import cleanup_old_uploads, get_history, get_result, save_result
from .disease_info import DISEASE_INFO, get_info
from .inference import predict
from .models_loader import load_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("porang")

app = Flask(__name__, template_folder=os.path.join(config.BASE_DIR, "templates"),
            static_folder=os.path.join(config.BASE_DIR, "static"))
app.config["UPLOAD_FOLDER"] = config.UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_MB * 1024 * 1024

model, model_trained = load_model()
cleanup_old_uploads(days=7)

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MONTHS_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def is_valid_image(path):
    with open(path, "rb") as f:
        head = f.read(12)
    if head[:3] == b"\xff\xd8\xff":
        return True
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return True
    return False


def format_time(dt):
    return f"{dt.day} {MONTHS_ID[dt.month - 1]} {dt.year}, {dt:%H:%M} WIB"


def compute_severity(disease, lesion_area, confidence):
    if "SEHAT" in (disease or "").upper():
        return {"label": "Sehat", "stage": "Tidak Ada Infeksi", "tone": "optimal"}

    area = float(lesion_area or 0)
    if area >= 15:
        return {"label": "Berat", "stage": "Stadium 3", "tone": "critical"}
    if area >= 5:
        return {"label": "Sedang", "stage": "Stadium 2", "tone": "moderate"}
    return {"label": "Ringan", "stage": "Stadium 1", "tone": "optimal"}


def confidence_label(confidence):
    if confidence >= 85:
        return "Tingkat Keyakinan Sangat Tinggi"
    if confidence >= 65:
        return "Tingkat Keyakinan Tinggi"
    if confidence >= 45:
        return "Tingkat Keyakinan Sedang"
    return "Tingkat Keyakinan Rendah"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": config.MODEL_NAME,
        "trained": bool(model_trained),
        "classes": config.CLASS_NAMES,
    })


@app.route("/predict", methods=["POST"])
def predict_route():
    if not model_trained or model is None:
        return jsonify({
            "status": "error",
            "message": "Model belum tersedia. Letakkan file model di folder models/.",
        }), 503

    if "image" not in request.files:
        return jsonify({"status": "error", "message": "Tidak ada gambar"}), 400

    f = request.files["image"]
    if not f or f.filename == "":
        return jsonify({"status": "error", "message": "File kosong"}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"status": "error", "message": "Format tidak didukung"}), 400

    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(config.UPLOAD_DIR, filename)
    f.save(path)

    if not is_valid_image(path):
        try:
            os.remove(path)
        except OSError:
            pass
        return jsonify({"status": "error", "message": "File bukan gambar valid"}), 400

    ok, reason = is_porang_leaf(path)
    if not ok:
        try:
            os.remove(path)
        except OSError:
            pass
        return jsonify({"status": "error", "message": reason}), 400

    try:
        pred = predict(model, path)
        if pred["confidence"] < config.MIN_PREDICTION_CONFIDENCE:
            try:
                os.remove(path)
            except OSError:
                pass
            return jsonify({
                "status": "error",
                "message": (
                    "Model tidak dapat mengidentifikasi citra sebagai daun porang. "
                    "Pastikan citra berupa daun porang yang jelas."
                ),
            }), 400
        # Margin: porang asli memiliki kelas dominan yang jelas
        all_probs = sorted(pred["all"].values(), reverse=True)
        if len(all_probs) >= 2 and (all_probs[0] - all_probs[1]) < 15:
            try:
                os.remove(path)
            except OSError:
                pass
            return jsonify({
                "status": "error",
                "message": (
                    "Model tidak yakin citra ini adalah daun porang. "
                    "Pastikan citra berupa daun porang yang jelas."
                ),
            }), 400
        analysis = analyze_image(path)
        info = get_info(pred["disease"])
        severity = compute_severity(
            pred["disease"], analysis["lesion_area"], pred["confidence"]
        )

        now = datetime.now()
        result = {
            "status": "success",
            "diagnosis_id": f"PRG-{uuid.uuid4().hex[:5].upper()}",
            "model": config.MODEL_NAME,
            "disease": pred["disease"],
            "display_disease": info["display_name"],
            "confidence": pred["confidence"],
            "confidence_label": confidence_label(pred["confidence"]),
            "all": pred["all"],
            "severity": severity,
            "time": format_time(now),
            "image": {
                "filename": filename,
                "url": f"/uploads/{filename}",
                "width": analysis["width"],
                "height": analysis["height"],
                "resolution": analysis["resolution"],
            },
            "analysis": {
                "lesion_area": analysis["lesion_area"],
                "boxes": analysis["boxes"],
                "box_count": analysis["box_count"],
                "heatmap": analysis["heatmap"],
                "quality": analysis["quality"],
            },
            "info": info,
        }

        save_result(result)
        log.info(
            "predict %s -> %s %.1f%% severity=%s area=%.1f%%",
            filename, pred["disease"], pred["confidence"],
            severity["label"], analysis["lesion_area"],
        )
        return jsonify(result)
    except Exception as exc:  # noqa: BLE001
        log.exception("predict failed")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/riwayat", methods=["GET"])
def api_riwayat():
    try:
        limit = max(1, min(int(request.args.get("limit", 20)), 100))
    except ValueError:
        limit = 20
    return jsonify({"status": "success", "data": get_history(limit)})


@app.route("/api/riwayat/<diagnosis_id>", methods=["GET"])
def api_riwayat_detail(diagnosis_id):
    result = get_result(diagnosis_id)
    if not result:
        return jsonify({"status": "error", "message": "Riwayat tidak ditemukan"}), 404
    return jsonify(result)


@app.route("/api/panduan", methods=["GET"])
def api_panduan():
    data = []
    for key, info in DISEASE_INFO.items():
        item = {"key": key}
        item.update(info)
        data.append(item)
    return jsonify({"status": "success", "data": data})


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    safe = os.path.basename(filename)
    if not os.path.exists(os.path.join(config.UPLOAD_DIR, safe)):
        abort(404)
    return send_from_directory(config.UPLOAD_DIR, safe)


@app.errorhandler(413)
def too_large(_):
    return jsonify({
        "status": "error",
        "message": f"Ukuran file melebihi {config.MAX_UPLOAD_MB}MB",
    }), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=True)
