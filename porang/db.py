import json
import os
import sqlite3
import time

from . import config

DB_PATH = os.path.join(config.BASE_DIR, "porang.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS riwayat_prediksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diagnosis_id TEXT,
    nama_file TEXT,
    image_filename TEXT,
    hasil_prediksi TEXT,
    confidence REAL,
    severity TEXT,
    lesion_area REAL,
    model TEXT,
    probabilitas TEXT,
    detail TEXT,
    waktu_lokal TEXT,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

_MIGRATIONS = [
    ("diagnosis_id", "TEXT"),
    ("image_filename", "TEXT"),
    ("severity", "TEXT"),
    ("lesion_area", "REAL"),
    ("detail", "TEXT"),
    ("waktu_lokal", "TEXT"),
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute(_SCHEMA)
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(riwayat_prediksi)")}
    for name, ddl in _MIGRATIONS:
        if name not in cols:
            conn.execute(f"ALTER TABLE riwayat_prediksi ADD COLUMN {name} {ddl}")
    conn.commit()
    conn.close()


def save_result(result):
    image = result.get("image", {})
    conn = get_conn()
    conn.execute(
        """INSERT INTO riwayat_prediksi
           (diagnosis_id, nama_file, image_filename, hasil_prediksi, confidence,
            severity, lesion_area, model, probabilitas, detail, waktu_lokal)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            result.get("diagnosis_id"),
            image.get("filename"),
            image.get("filename"),
            result.get("disease"),
            result.get("confidence"),
            (result.get("severity") or {}).get("label"),
            (result.get("analysis") or {}).get("lesion_area"),
            result.get("model"),
            json.dumps(result.get("all", {})),
            json.dumps(result, ensure_ascii=False),
            result.get("time"),
        ),
    )
    conn.commit()
    conn.close()


def get_history(limit=20):
    conn = get_conn()
    rows = conn.execute(
        """SELECT id, diagnosis_id, hasil_prediksi, confidence, severity,
                  lesion_area, model, image_filename, waktu_lokal, waktu
           FROM riwayat_prediksi ORDER BY id DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    conn.close()

    data = []
    for row in rows:
        item = dict(row)
        item["image_url"] = (
            f"/uploads/{item['image_filename']}" if item.get("image_filename") else None
        )
        data.append(item)
    return data


def get_result(diagnosis_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT detail FROM riwayat_prediksi WHERE diagnosis_id = ? ORDER BY id DESC LIMIT 1",
        (diagnosis_id,),
    ).fetchone()
    conn.close()
    if not row or not row["detail"]:
        return None
    try:
        return json.loads(row["detail"])
    except Exception:
        return None


def cleanup_old_uploads(days=7):
    cutoff = time.time() - days * 86400
    conn = get_conn()
    try:
        for name in os.listdir(config.UPLOAD_DIR):
            path = os.path.join(config.UPLOAD_DIR, name)
            if not os.path.isfile(path):
                continue
            if os.path.getmtime(path) < cutoff:
                try:
                    os.remove(path)
                except OSError:
                    continue
                conn.execute(
                    "DELETE FROM riwayat_prediksi WHERE image_filename = ?", (name,)
                )
        conn.commit()
    finally:
        conn.close()


init_db()
