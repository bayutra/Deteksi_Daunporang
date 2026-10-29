"""Analisis citra: kualitas foto, deteksi area lesi, dan heatmap overlay.

Catatan: deteksi lesi memakai segmentasi warna (heuristic) untuk kebutuhan
visualisasi. Ini bukan model object-detection terlatih, sehingga hasilnya
bersifat indikatif dan dipakai sebagai pendukung tampilan diagnosis.
"""

import base64

import cv2
import numpy as np

from . import config

MAX_BOXES = 6


def _quality(gray):
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(gray.mean())

    if sharpness >= 220:
        focus, focus_tone = "Tajam", "optimal"
    elif sharpness >= 70:
        focus, focus_tone = "Cukup Tajam", "moderate"
    else:
        focus, focus_tone = "Buram", "critical"

    if 55 <= brightness <= 195:
        exposure, exposure_tone = "Pencahayaan Baik", "optimal"
    elif brightness < 55:
        exposure, exposure_tone = "Kurang Cahaya", "critical"
    else:
        exposure, exposure_tone = "Terlalu Terang", "moderate"

    tone = "optimal"
    if "critical" in (focus_tone, exposure_tone):
        tone = "critical"
    elif "moderate" in (focus_tone, exposure_tone):
        tone = "moderate"

    return {
        "focus": focus,
        "focus_tone": focus_tone,
        "exposure": exposure,
        "exposure_tone": exposure_tone,
        "sharpness": round(sharpness, 1),
        "brightness": round(brightness, 1),
        "tone": tone,
    }


def _lesion_mask(hsv, shape):
    h, w = shape[:2]
    # Cokelat / kuning / amber (lesi kering dan halo klorotik)
    amber = cv2.inRange(hsv, (5, 55, 30), (38, 255, 255))
    # Pusat nekrotik cokelat gelap
    dark = cv2.inRange(hsv, (0, 45, 12), (32, 255, 110))
    mask = cv2.bitwise_or(amber, dark)

    # Batasi pada area yang berdekatan dengan jaringan hijau (daun)
    green = cv2.inRange(hsv, (30, 35, 25), (98, 255, 255))
    green = cv2.morphologyEx(
        green, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max(5, w // 40) | 1,) * 2),
    )
    green = cv2.dilate(
        green, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max(5, w // 25) | 1,) * 2)
    )

    mask = cv2.bitwise_and(mask, green)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
    )
    return mask, green


def _heatmap_data(mask):
    h, w = mask.shape[:2]
    overlay = np.zeros((h, w, 4), dtype=np.uint8)
    # Amber pekat dengan alpha, cukup untuk overlay transparan.
    overlay[mask > 0] = (11, 158, 245, 155)
    overlay = cv2.GaussianBlur(overlay, (0, 0), sigmaX=max(1, w // 400))

    max_w = 900
    if w > max_w:
        scale = max_w / w
        overlay = cv2.resize(overlay, (max_w, max(1, int(h * scale))),
                             interpolation=cv2.INTER_AREA)

    ok, buf = cv2.imencode(".png", overlay)
    if not ok:
        return None
    return "data:image/png;base64," + base64.b64encode(buf).decode("ascii")


def analyze_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Cannot read image: {path}")

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Kualitas dihitung dari citra asli, mask lesi dari versi kecil agar cepat.
    quality = _quality(gray)

    max_dim = 1024
    scale = min(1.0, max_dim / max(w, h))
    work = img
    if scale < 1.0:
        work = cv2.resize(img, (int(w * scale), int(h * scale)),
                          interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(work, cv2.COLOR_BGR2HSV)
    mask, green = _lesion_mask(hsv, work.shape)

    wh, ww = work.shape[:2]
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = max(60, int(ww * wh * 0.0004))
    found = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        # Abaikan kotak yang terlalu tipis / tidak wajar.
        if bw < ww * 0.01 or bh < wh * 0.01:
            continue
        found.append((area, x, y, bw, bh))

    found.sort(key=lambda t: t[0], reverse=True)
    found = found[:MAX_BOXES]

    boxes = []
    for i, (area, x, y, bw, bh) in enumerate(found):
        boxes.append({
            "label": f"Lesi {chr(65 + i)}",
            "x": round(x / ww * 100, 2),
            "y": round(y / wh * 100, 2),
            "w": round(bw / ww * 100, 2),
            "h": round(bh / wh * 100, 2),
            "area_pct": round(area / (ww * wh) * 100, 2),
        })

    leaf_pixels = int(cv2.countNonZero(cv2.bitwise_or(green, mask)))
    lesion_pixels = int(cv2.countNonZero(mask))
    area_pct = lesion_pixels / max(leaf_pixels, 1) * 100
    area_pct = round(min(area_pct, 85.0), 1)

    return {
        "width": w,
        "height": h,
        "resolution": f"{w * h / 1_000_000:.1f} MP ({w}x{h} px)",
        "quality": quality,
        "lesion_area": area_pct,
        "boxes": boxes,
        "box_count": len(boxes),
        "heatmap": _heatmap_data(mask),
    }


def is_porang_leaf(path):
    """Heuristik: pastikan citra mengandung daun hijau yang jelas.

    Mengembalikan (ok, pesan). Hanya citra dengan area hijau signifikan
    (daun) yang dianggap layak dianalisis oleh sistem khusus porang.
    """
    img = cv2.imread(path)
    if img is None:
        return False, "File bukan gambar valid."

    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Rentang hijau daun (porang) — cukup longgar agar daun sakit tetap lolos.
    green = cv2.inRange(hsv, (25, 35, 25), (100, 255, 255))

    green_frac = cv2.countNonZero(green) / float(w * h)
    contours, _ = cv2.findContours(green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max((cv2.contourArea(c) for c in contours), default=0.0)
    largest_frac = largest / float(w * h)

    # Bounding box daun hijau terbesar: porang berdaun lebar, bukan memanjang
    # seperti daun padi/rumput, dan tidak tersebar seperti latar mobil.
    largest_contour = max(contours, key=cv2.contourArea, default=None)
    if largest_contour is not None:
        x, y, bw, bh = cv2.boundingRect(largest_contour)
        aspect = bh / max(bw, 1)
    else:
        aspect = 1.0

    # Tekstur: citra daun asli memiliki tepi/vena. Citra polos (warna solid)
    # atau grafik sederhana ditolak.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_frac = cv2.countNonZero(edges) / float(w * h)
    if edge_frac < 0.008 or gray.std() < 10.0:
        return False, (
            "Citra tidak memiliki tekstur daun yang jelas. "
            "Sistem hanya menganalisis daun porang."
        )

    if green_frac < getattr(config, "MIN_LEAF_GREEN_FRACTION", 0.08):
        return False, (
            "Gambar bukan daun porang / bukan citra daun. "
            "Sistem hanya menganalisis daun porang."
        )
    if largest_frac < getattr(config, "MIN_LEAF_REGION_FRACTION", 0.04):
        return False, (
            "Area daun porang tidak cukup jelas. "
            "Sistem hanya menganalisis daun porang."
        )
    # Daun porang lebar; daun padi/rumput memanjang (aspect tinggi) ditolak.
    if aspect > 2.2 or aspect < 0.4:
        return False, (
            "Bentuk daun tidak sesuai daun porang. "
            "Sistem hanya menganalisis daun porang."
        )
    return True, ""
