# PorangAI Precision Agro

Sistem web deteksi penyakit daun porang berbasis **EfficientNetB0** dengan antarmuka
bergaya *AgriTech Telemetry & Precision Farming*. Aplikasi berjalan sepenuhnya di
browser (web only) dan menggunakan database SQL (SQLite) untuk menyimpan riwayat
diagnosis.

## Daftar Isi

1. [Fitur](#fitur)
2. [Arsitektur](#arsitektur)
3. [Struktur Folder](#struktur-folder)
4. [Prasyarat](#prasyarat)
5. [Instalasi & Menjalankan](#instalasi--menjalankan)
6. [Konfigurasi (.env)](#konfigurasi-env)
7. [Model](#model)
8. [Alur Penggunaan](#alur-penggunaan)
9. [Penjelasan Halaman & Komponen UI](#penjelasan-halaman--komponen-ui)
10. [Analisis Citra & Guard Porang-Only](#analisis-citra--guard-porang-only)
11. [Basis Pengetahuan Penyakit](#basis-pengetahuan-penyakit)
12. [Database & Riwayat](#database--riwayat)
13. [Endpoint API](#endpoint-api)
14. [Aksesibilitas & Responsivitas](#aksesibilitas--responsivitas)
15. [Pengujian](#pengujian)
16. [Catatan Produksi](#catatan-produksi)

---

## Fitur

### Input & Deteksi
- Unggah foto / drag-and-drop (JPG, PNG, WEBP, maks 5MB).
- Tombol **Gunakan Contoh** untuk mencoba citra contoh (`static/img/sample_leaf.jpg`).
- Validasi tipe file (magic bytes), ukuran, dan status model di sisi server.
- Overlay **Bounding Box** area lesi + **Heatmap Lesi** (segmentasi warna, indikatif).
- Zoom, layar penuh, dan metadata resolusi/kualitas citra.
- Panel unggah disusun **kiri-kanan** (dropzone kiri, preview kanan) agar ringkas.
- Preview gambar dibatasi (maks 280px tinggi) agar tidak terlalu besar.

### Laporan Diagnosis
- Kartu klasifikasi: penyakit, nama latin, tingkat keparahan, skor keyakinan.
- Gauge keyakinan (SVG circular), dampak terhadap glukomanan, dan 3 metrik risiko.
- Tab **Gejala & Faktor Penyebab**, **Rekomendasi Penanganan & Solusi**,
  **Langkah Pencegahan & Budidaya**.
- Tombol **Unduh Laporan PDF** (dialog cetak browser → *Save as PDF*).
- Tombol **Bagikan** (Web Share API / salin ringkasan ke clipboard).
- **Pindai Gambar Lain** untuk kembali ke halaman input.

### Riwayat & Penyimpanan
- Database SQL (SQLite) menyimpan diagnosis, confidence, severity, area lesi,
  probabilitas, dan detail JSON.
- Tab **Riwayat** terpisah (bukan di bawah analisis AI) dengan thumbnail;
  klik untuk membuka kembali laporan (tombol "Kembali ke Riwayat").
- File upload dibersihkan otomatis setelah 7 hari.

### UI/UX
- Design system AgriTech: palet hijau, *Plus Jakarta Sans* + *Inter*,
  *Material Symbols*, dan token warna/spasi konsisten.
- Mode gelap, toast notification, loading state, empty/error state.
- Responsif (desktop/tablet/mobile), fokus keyboard, `aria-*`, skip link.
- Halaman **Panduan Agronomi** (modal) berisi ensiklopedia tiga kelas penyakit.
- Modal **Bantuan** dengan langkah penggunaan.

---

## Arsitektur

```
Browser (HTML/CSS/JS)
   │  fetch /predict, /api/riwayat, /api/panduan
   ▼
Flask (app.py)
   ├─ models_loader.py  → EfficientNetB0 (.keras)
   ├─ inference.py      → preprocessing + predict
   ├─ analysis.py       → kualitas citra, deteksi lesi, heatmap, guard porang
   ├─ disease_info.py   → basis pengetahuan penyakit
   └─ db.py             → SQLite (riwayat_prediksi)
```

Frontend adalah SPA ringan: tiga view (`scanView`, `historyView`, `resultView`)
yang ditampilkan/sembunyikan via JavaScript. Navigasi atas (`Analisis Citra AI`,
`Riwayat`, `Panduan Agronomi`) mengganti view aktif.

---

## Struktur Folder

```
web_porang/
├─ app.py                  # entrypoint (shim ke paket porang)
├─ porang/                 # paket inti
│  ├─ __init__.py
│  ├─ app.py               # Flask routes & orkestrasi
│  ├─ config.py            # konfigurasi path/kelas/env/threshold
│  ├─ analysis.py          # kualitas citra, deteksi lesi, heatmap, guard porang
│  ├─ disease_info.py      # basis pengetahuan penyakit (3 kelas)
│  ├─ inference.py         # preprocessing + prediksi model
│  ├─ models_loader.py     # loader model EfficientNetB0
│  └─ db.py                # SQLite: riwayat & cleanup
├─ templates/
│  └─ index.html           # markup utama
├─ static/
│  ├─ css/style.css        # design system & responsif
│  ├─ js/app.js            # controller frontend
│  └─ img/sample_leaf.jpg  # citra contoh
├─ models/                 # file model (.keras) + class_indices.json (opsional)
├─ uploads/                # file upload (auto-cleanup 7 hari)
├─ docs/
│  └─ ANALISIS_WEB.md      # analisis gap web
├─ tests/test_basic.py     # tes dasar
├─ porang.db               # database SQLite (auto-dibuat)
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Prasyarat

- Python 3.10+ (diuji dengan 3.12)
- TensorFlow / Keras (untuk memuat model `.keras`)
- OpenCV, NumPy, Pillow, Flask, python-dotenv, pytest

---

## Instalasi & Menjalankan

```bash
cd "D:\Kuliah\SEMESTER 7\SISDAS\web_porang"
pip install -r requirements.txt
python app.py
```

Buka `http://localhost:5000`.

Untuk produksi, jalankan dengan WSGI server (mis. `gunicorn app:app`) dan
pertimbangkan autentikasi/rate limiting.

---

## Konfigurasi (.env)

Salin `.env.example` menjadi `.env` dan sesuaikan:

```env
MODEL_PATH=D:\Kuliah\SEMESTER 7\SISDAS\web_porang\models\baseline_porang.keras
MAX_UPLOAD_MB=5
PORT=5000
MIN_LEAF_GREEN_FRACTION=0.08
MIN_LEAF_REGION_FRACTION=0.04
MIN_PREDICTION_CONFIDENCE=60.0
```

- `MODEL_PATH`: path absolut ke file model.
- `MAX_UPLOAD_MB`: batas ukuran upload.
- `PORT`: port server.
- `MIN_LEAF_GREEN_FRACTION`: ambang fraksi piksel hijau (guard porang).
- `MIN_LEAF_REGION_FRACTION`: ambang region daun kontigu.
- `MIN_PREDICTION_CONFIDENCE`: ambang keyakinan model (0–100).

---

## Model

Letakkan file model di `models/` dengan salah satu nama berikut:

- `baseline_porang.keras` (utama)
- `efficientnet_porang.keras`
- `model_porang.keras`

Opsional: `models/class_indices.json` untuk memetakan urutan kelas output model.

Kelas default: `DAUN SEHAT`, `HAWAR DAUN`, `KARAT BERCAK`.

Model tunggal berbasis **EfficientNetB0** (bukan VGG16/Fusion).

---

## Alur Penggunaan

1. Buka halaman utama (tab *Analisis Citra AI*).
2. Pilih metode input:
   - **Unggah Foto**: klik/seret gambar ke dropzone, atau gunakan **Gunakan Contoh**.
3. Klik **Deteksi dari File**.
4. Sistem memvalidasi gambar, menjalankan guard porang, lalu klasifikasi.
5. Hasil tampil di tab laporan: klasifikasi, gauge, metrik, tab detail, overlay lesi.
6. Unduh laporan (PDF via cetak), bagikan, atau **Pindai Gambar Lain**.
7. Tab **Riwayat** menampilkan daftar diagnosis tersimpan; klik untuk membuka
   kembali laporan (tombol "Kembali ke Riwayat").
8. Tab **Panduan Agronomi** berisi ensiklopedia tiga kelas penyakit.

---

## Penjelasan Halaman & Komponen UI

### Top App Bar
- Brand *PorangAI Precision Agro*.
- Pill status model (EfficientNetB0: Aktif).
- Navigasi: Analisis Citra AI, Riwayat, Panduan Agronomi.
- Aksi: Mode Lokal, Bantuan, Mode gelap/terang, Pindai Citra Baru, avatar.

### Sub-Header
- Breadcrumb, judul halaman, badge ID, strip telemetry (tanggal, kualitas citra, model).

### View: Analisis Citra AI
- Hero card dengan poin fitur dan contoh citra.
- Panel unggah (kiri-kanan): dropzone (kiri) + preview (kanan), tombol deteksi.
- Tips (pencahayaan, fokus, latar).

### View: Riwayat
- Kartu riwayat dengan thumbnail, kelas, confidence, severity, waktu.
- Klik baris → buka laporan lengkap.

### View: Hasil Diagnosis
- **Viewport Deteksi Lesi**: toolbar (Bounding Box, Heatmap Lesi, zoom, fullscreen),
  stage dengan gambar + overlay box + heatmap + scanline, metadata bar
  (resolusi, area terdampak, kualitas).
- **Kartu Ringkasan**: kategori, penyakit, latin, badge keparahan, gauge
  keyakinan, dampak glukomanan, 3 metrik, tombol protokol.
- **Tab Detail**: 3 kolom kartu (gejala, rekomendasi, pencegahan).
- **Bottom Action Bar**: status simpan, Unduh PDF, Bagikan, Pindai Gambar Lain.

### Modal
- **Panduan Agronomi**: ensiklopedia 3 kelas (gejala, rekomendasi, pencegahan).
- **Bantuan**: langkah penggunaan + catatan.

---

## Analisis Citra & Guard Porang-Only

### Kualitas Citra (`analysis.py::_quality`)
- Ketajaman via varians Laplacian → Tajam / Cukup Tajam / Buram.
- Pencahayaan via rata-rata grayscale → Baik / Kurang Cahaya / Terlalu Terang.

### Deteksi Lesi (heuristik segmentasi warna)
- Mask lesi: cokelat/amber/kuning + pusat nekrotik, dibatasi pada area
  berdekatan jaringan hijau (daun).
- Morfologi open/close, kontur, top 6 bounding box (ternormalisasi %).
- Area terdampak = piksel lesi / piksel daun × 100 (clamp 85%).
- Heatmap overlay (PNG transparan base64, max 900px).

> Deteksi lesi bersifat **indikatif** (segmentasi warna), bukan model
> object detection terlatih. Label "Overlay lesi: segmentasi warna (indikatif)".

### Guard Porang-Only (`analysis.is_porang_leaf`)
1. Fraksi piksel hijau daun ≥ `MIN_LEAF_GREEN_FRACTION` (default 8%).
2. Region hijau kontigu terbesar ≥ `MIN_LEAF_REGION_FRACTION` (default 4%).
3. Tekstur: edge density (Canny) ≥ 0.8% dan std grayscale ≥ 10.
4. Bentuk: aspek rasio bounding box daun 0.4–2.2 (menolak daun memanjang
   seperti padi/rumput).
5. Setelah prediksi: keyakinan ≥ `MIN_PREDICTION_CONFIDENCE` (default 60%).
6. Margin antar kelas teratas ≥ 15 poin.

Citra yang tidak lolos guard ditolak (HTTP 400) dengan pesan yang sesuai dan
file upload dihapus.

---

## Basis Pengetahuan Penyakit

`disease_info.py` memuat untuk tiap kelas:
- `display_name`, `latin`, `category`, `short`
- `impact_title`, `impact` (HTML terpercaya)
- `confidence_note`
- `metrics` (3 metrik: risiko penularan, organ terdampak, defisit umbi)
- `symptoms` (3 kartu: ikon, judul, teks, catatan)
- `recommendations` (3 kartu: tag, tone, ikon, judul, teks, detail, footnote)
- `prevention` (3 kartu: ikon, judul, teks)

Kelas:
- **DAUN SEHAT**: tidak ada patogen, jaringan normal, fotosintesis optimal.
- **HAWAR DAUN**: *Phytophthora* / *Xanthomonas*, bercak basah, cepat menular
  via air & tanah, defisit umbi 20–40%.
- **KARAT BERCAK**: *Cercospora*, lesi konsentris dengan halo klorotik, defisit
  umbi 12–25%.

---

## Database & Riwayat

Tabel `riwayat_prediksi` (SQLite, `porang.db`):

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| diagnosis_id | TEXT | PRG-XXXXX |
| nama_file | TEXT | Nama file upload |
| image_filename | TEXT | Nama file di uploads/ |
| hasil_prediksi | TEXT | Kelas prediksi |
| confidence | REAL | Keyakinan (%) |
| severity | TEXT | Sehat/Ringan/Sedang/Berat |
| lesion_area | REAL | Area lesi (%) |
| model | TEXT | Nama model |
| probabilitas | TEXT | JSON probabilitas per kelas |
| detail | TEXT | JSON hasil lengkap |
| waktu_lokal | TEXT | Waktu format Indonesia |
| waktu | TIMESTAMP | UTC default |

- `init_db()` membuat tabel + migrasi kolom otomatis (ALTER TABLE).
- `save_result()`, `get_history()`, `get_result()`, `cleanup_old_uploads(days=7)`.
- Riwayat ditampilkan di tab **Riwayat** dengan thumbnail; klik membuka laporan
  (tombol "Kembali ke Riwayat").

---

## Endpoint API

| Method | Path | Keterangan |
|---|---|---|
| GET | `/` | Halaman utama |
| GET | `/health` | Status model & kelas |
| POST | `/predict` | Upload citra → hasil diagnosis (multipart `image`) |
| GET | `/api/riwayat?limit=10` | Daftar riwayat |
| GET | `/api/riwayat/<diagnosis_id>` | Detail riwayat |
| GET | `/api/panduan` | Data panduan agronomi |
| GET | `/uploads/<filename>` | Citra hasil upload |

### Contoh respons `/predict` (sukses)

```json
{
  "status": "success",
  "diagnosis_id": "PRG-ABC12",
  "model": "EfficientNetB0",
  "disease": "KARAT BERCAK",
  "display_disease": "Bercak Daun (Karat)",
  "confidence": 89.6,
  "confidence_label": "Tingkat Keyakinan Sangat Tinggi",
  "all": { "DAUN SEHAT": 2.0, "HAWAR DAUN": 8.4, "KARAT BERCAK": 89.6 },
  "severity": { "label": "Sedang", "stage": "Stadium 2", "tone": "moderate" },
  "time": "29 Oktober 2026, 13:00 WIB",
  "image": { "filename": "...jpg", "url": "/uploads/...jpg", "width": 1100, "height": 821, "resolution": "0.9 MP (1100x821 px)" },
  "analysis": {
    "lesion_area": 9.7,
    "boxes": [{ "label": "Lesi A", "x": 12.3, "y": 20.1, "w": 18.4, "h": 22.0, "area_pct": 3.8 }],
    "box_count": 6,
    "heatmap": "data:image/png;base64,...",
    "quality": { "focus": "Tajam", "exposure": "Pencahayaan Baik", "tone": "optimal", ... }
  },
  "info": { "category": "...", "latin": "...", "impact": "...", "metrics": [...], "symptoms": [...], "recommendations": [...], "prevention": [...] }
}
```

### Error (guard porang / validasi)

```json
{ "status": "error", "message": "Gambar bukan daun porang / bukan citra daun. Sistem hanya menganalisis daun porang." }
```

HTTP 400 (validasi/guard) atau 503 (model tidak tersedia).

---

## Aksesibilitas & Responsivitas

- Skip link, `aria-live` pada toast, `role="tablist"`/`aria-selected` pada mode & tab.
- Fokus keyboard pada dropzone (`Enter`/`Space`).
- `:focus-visible` outline.
- Touch target ≥ 44px pada mobile.
- Breakpoint: 1280px (model pill), 1024px (nav), 760px (mobile), 420px (extra small).
- Mode gelap (`body.dark`) dengan token warna override.
- `prefers-reduced-motion` menonaktifkan animasi.
- Print CSS: menyembunyikan app bar/bottom bar/toolbar, menampilkan semua tab panel dengan judul section.

---

## Pengujian

```bash
cd "D:\Kuliah\SEMESTER 7\SISDAS\web_porang"
python -m pytest tests/ -q
```

Tes (`tests/test_basic.py`):
- `test_health_endpoint`: `/health` mengembalikan status ok.
- `test_predict_no_file`: `/predict` tanpa file → 400.
- `test_preprocess_shape`: preprocessing menghasilkan shape (1, 224, 224, 3).

Verifikasi manual yang dilakukan:
- Import `app` berhasil (EXIT 0).
- Browser test (desktop & mobile): tidak ada error konsol, 0 404.
- Alur unggah contoh → hasil + riwayat + detail + kembali.
- Alur kamera dihapus; hanya unggah.
- Guard porang: citra non-daun ditolak; daun porang asli lolos.
- Media cetak (print) tervalidasi.

---

## Deployment (Public)

Aplikasi dapat dideploy secara publik. Karena menggunakan TensorFlow + model 50MB,
disarankan platform yang mendukung container atau ML.

### Opsi 1 — Hugging Face Spaces (gratis, direkomendasikan untuk ML)

1. Buat Space baru di https://huggingface.co/spaces → pilih **Docker**.
2. Clone repo Space, salin isi proyek (atau push repo ini).
3. Pastikan `Dockerfile` ada di root Space.
4. Space akan build & run otomatis di port 7860.
5. Aplikasi publik di `https://huggingface.co/spaces/<user>/<space>`.

### Opsi 2 — Render (gratis/paid)

1. Push repo ke GitHub.
2. Di Render: **New → Web Service** → pilih repo.
3. Render mendeteksi `Dockerfile` (atau gunakan `Procfile`).
4. Set environment variables: `MODEL_PATH`, `MAX_UPLOAD_MB`, dll.
5. Deploy. (Free tier sleep setelah 15 menit idle; TensorFlow cold start ~30–60s.)

### Opsi 3 — VPS (DigitalOcean, AWS EC2, dll.)

```bash
git clone https://github.com/bayutra/Deteksi_Daunporang.git
cd Deteksi_Daunporang
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Jalankan dengan gunicorn di belakang (systemd/supervisor)
gunicorn app:app --bind 0.0.0.0:8000 --workers 1 --timeout 120
```

Gunakan Nginx sebagai reverse proxy + HTTPS (Let's Encrypt).

### Catatan Deployment

- **Filesystem ephemeral**: Di Render/Cloud Run, `porang.db` dan `uploads/` hilang
  saat redeploy. Untuk produksi, gunakan database terkelola (PostgreSQL/Supabase)
  atau volume persisten. Untuk demo, SQLite cukup.
- **Memori**: TensorFlow membutuhkan ~500MB+ RAM. Gunakan 1 worker gunicorn.
- **Cold start**: model dimuat saat startup (~10–30s). Set timeout gunicorn ≥ 120s.
- **Git LFS**: untuk menghindari warning file besar, gunakan Git LFS untuk
  `models/baseline_porang.keras`:
  ```bash
  git lfs install
  git lfs track "models/*.keras"
  git add .gitattributes models/baseline_porang.keras
  git commit -m "Track model with LFS"
  git push
  ```
- **Environment**: set `MODEL_PATH` absolut sesuai path di server, atau biarkan
  auto-detect (`models/baseline_porang.keras` relatif ke root).

- Sistem **khusus untuk daun porang**. Citra yang bukan daun porang (atau tidak jelas) ditolak oleh guard heuristik (area hijau daun, tekstur, bentuk) dan ambang keyakinan model. Guard ini **heuristik**, bukan detektor porang terlatih; citra daun hijau lain (mis. padi) dengan tekstur bisa lolos. Untuk deteksi porang yang benar-benar ketat, diperlukan model biner/OOD terlatih.
- Deteksi lesi memakai segmentasi warna untuk visualisasi, **bukan** model
  object detection terlatih. Gunakan sebagai indikator pendukung, bukan dasar
  tunggal keputusan agronomi.
- Untuk produksi, jalankan dengan WSGI (mis. `gunicorn app:app`) dan pertimbangkan
  autentikasi/rate limiting/CSRF.
- File upload dibersihkan otomatis setelah 7 hari (`cleanup_old_uploads`).
- Model dimuat sekali saat startup; pastikan file model tersedia sebelum run.