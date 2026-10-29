/* ============================================================
   PorangAI Precision Agro - Frontend Controller
   ============================================================ */

const $ = (id) => document.getElementById(id);
const MONTHS_ID = [
  "Januari", "Februari", "Maret", "April", "Mei", "Juni",
  "Juli", "Agustus", "September", "Oktober", "November", "Desember",
];

let currentResult = null;
let zoom = 1;
let bboxVisible = true;
let guideLoaded = false;
let resultSource = "scan";

/* ---------------- Elements ---------------- */
const preview = $("preview");
const previewPlaceholder = $("previewPlaceholder");
const fileInput = $("fileInput");
const dropzone = $("dropzone");
const uploadBtn = $("uploadBtn");
const sampleBtn = $("sampleBtn");
const scanStatus = $("scanStatus");
const previewWrap = $("previewWrap");

const scanView = $("scanView");
const historyView = $("historyView");
const resultView = $("resultView");
const bottomBar = $("bottomBar");
const historyList = $("historyList");
const refreshHistory = $("refreshHistory");

const breadcrumb = $("breadcrumb");
const pageTitle = $("pageTitle");
const pageBadge = $("pageBadge");
const telemetryStrip = $("telemetryStrip");

const imageFrame = $("imageFrame");
const viewerStage = $("viewerStage");
const viewerEmpty = $("viewerEmpty");
const resultImage = $("resultImage");
const heatmapLayer = $("heatmapLayer");
const bboxLayer = $("bboxLayer");
const toggleBbox = $("toggleBbox");
const bboxIcon = $("bboxIcon");
const toggleHeatmap = $("toggleHeatmap");
const heatmapIcon = $("heatmapIcon");
const inferenceBadge = $("inferenceBadge");
const reticle = $("reticle");
const metaRes = $("metaRes");
const metaArea = $("metaArea");
const metaQuality = $("metaQuality");

const resultBack = $("resultBack");
const backToHistory = $("backToHistory");
const resDisease = $("resDisease");
const resLatin = $("resLatin");
const severityBadge = $("severityBadge");
const severityText = $("severityText");
const resConfidence = $("resConfidence");
const resConfLabel = $("resConfLabel");
const resConfNote = $("resConfNote");
const gaugeProgress = $("gaugeProgress");
const gaugeText = $("gaugeText");
const impactTitle = $("impactTitle");
const impactText = $("impactText");
const metricGrid = $("metricGrid");
const tabPanelGejala = $("tabPanelGejala");
const tabPanelRekomendasi = $("tabPanelRekomendasi");
const tabPanelPencegahan = $("tabPanelPencegahan");

const toastEl = $("toast");
const themeToggle = $("themeToggle");
const guideModal = $("guideModal");
const helpModal = $("helpModal");
const guideContent = $("guideContent");

/* ---------------- Utilities ---------------- */
function pad(n) { return String(n).padStart(2, "0"); }

function nowText() {
  const d = new Date();
  return `${d.getDate()} ${MONTHS_ID[d.getMonth()]} ${d.getFullYear()}, ${pad(d.getHours())}:${pad(d.getMinutes())} WIB`;
}

function showToast(msg, type = "info") {
  toastEl.textContent = msg;
  toastEl.className = "toast show " + type;
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => toastEl.classList.remove("show"), 3200);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

/* ---------------- Theme ---------------- */
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark");
}
function syncThemeIcon() {
  const dark = document.body.classList.contains("dark");
  const icon = themeToggle.querySelector(".material-symbols-outlined");
  if (icon) icon.textContent = dark ? "light_mode" : "dark_mode";
  themeToggle.setAttribute("aria-label", dark ? "Mode terang" : "Mode gelap");
}
syncThemeIcon();
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  document.body.classList.contains("dark")
    ? localStorage.setItem("theme", "dark")
    : localStorage.setItem("theme", "light");
  syncThemeIcon();
});

/* ---------------- Navigation & views ---------------- */
const navLinks = document.querySelectorAll(".navlink");
function setNav(name) {
  navLinks.forEach((b) => b.classList.toggle("active", b.dataset.nav === name));
}

function scanHeader() {
  breadcrumb.innerHTML = `
    <span>Beranda</span>
    <span class="material-symbols-outlined">chevron_right</span>
    <span class="current">Analisis Citra AI</span>`;
  pageTitle.textContent = "Diagnosis Penyakit Daun Porang";
  pageBadge.textContent = "AI VISION";
  telemetryStrip.innerHTML = `
    <div class="chip"><span class="material-symbols-outlined">calendar_today</span><span>${nowText()}</span></div>
    <div class="chip"><span class="material-symbols-outlined">memory</span><span>EfficientNetB0 &middot; 3 Kelas</span></div>
    <div class="chip ok"><span class="material-symbols-outlined">verified</span><span>Model Aktif</span></div>`;
}

function showScan() {
  scanView.hidden = false;
  historyView.hidden = true;
  resultView.hidden = true;
  bottomBar.hidden = true;
  setNav("scan");
  scanHeader();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function historyHeader() {
  breadcrumb.innerHTML = `
    <span>Beranda</span>
    <span class="material-symbols-outlined">chevron_right</span>
    <span class="current">Riwayat Prediksi</span>`;
  pageTitle.textContent = "Riwayat Diagnosis";
  pageBadge.textContent = "RIWAYAT";
  telemetryStrip.innerHTML = `
    <div class="chip"><span class="material-symbols-outlined">calendar_today</span><span>${nowText()}</span></div>
    <div class="chip"><span class="material-symbols-outlined">memory</span><span>EfficientNetB0 &middot; 3 Kelas</span></div>`;
}

function showHistory() {
  scanView.hidden = true;
  resultView.hidden = true;
  historyView.hidden = false;
  bottomBar.hidden = true;
  setNav("history");
  historyHeader();
  loadHistory();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showGuide() {
  openModal(guideModal);
  setNav("guide");
  if (guideLoaded) return;
  guideContent.innerHTML = "<em>Memuat panduan...</em>";
  fetch("/api/panduan")
    .then((r) => r.json())
    .then((data) => {
      if (data.status !== "success") throw new Error("Gagal memuat panduan");
      guideContent.innerHTML = `<div class="guide-grid">${data.data.map(guideCard).join("")}</div>`;
      guideLoaded = true;
    })
    .catch(() => {
      guideContent.innerHTML = "<em>Gagal memuat panduan agronomi.</em>";
    });
}

function guideCard(info) {
  const symptoms = (info.symptoms || []).map((s) => `<li><strong>${escapeHtml(s.title)}:</strong> ${stripTags(s.text)}</li>`).join("");
  const recs = (info.recommendations || []).map((r) => `<li><strong>${escapeHtml(r.title)}:</strong> ${stripTags(r.text)}</li>`).join("");
  const prev = (info.prevention || []).map((p) => `<li><strong>${escapeHtml(p.title)}:</strong> ${stripTags(p.text)}</li>`).join("");
  return `
    <article class="guide-card">
      <div class="guide-card-head">
        <div>
          <h3>${escapeHtml(info.display_name)}</h3>
          <p class="latin">${escapeHtml(info.latin)}</p>
        </div>
      </div>
      <p class="hint" style="margin-top:.5rem">${escapeHtml(info.short)}</p>
      <div class="guide-section"><h4>Gejala &amp; Penyebab</h4><ul>${symptoms}</ul></div>
      <div class="guide-section"><h4>Rekomendasi Penanganan</h4><ul>${recs}</ul></div>
      <div class="guide-section"><h4>Pencegahan &amp; Budidaya</h4><ul>${prev}</ul></div>
    </article>`;
}

function stripTags(value) {
  return String(value ?? "").replace(/<[^>]*>/g, "");
}

document.querySelectorAll("[data-nav]").forEach((el) => {
  el.addEventListener("click", () => {
    const nav = el.dataset.nav;
    if (nav === "scan") showScan();
    else if (nav === "history") showHistory();
    else if (nav === "guide") showGuide();
  });
});

$("newScanTop").addEventListener("click", () => showScan());
$("newScanBottom").addEventListener("click", () => showScan());
$("helpBtn").addEventListener("click", () => openModal(helpModal));

/* ---------------- Upload ---------------- */
function showPreview(blob) {
  if (preview.src) URL.revokeObjectURL(preview.src);
  preview.src = URL.createObjectURL(blob);
  preview.style.display = "block";
  previewPlaceholder.style.display = "none";
}

dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    fileInput.click();
  }
});
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("drag");
});
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("drag"));
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("drag");
  const file = e.dataTransfer.files[0];
  if (!file) return;
  fileInput.files = e.dataTransfer.files;
  validateAndPreview(file);
});
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) validateAndPreview(file);
});

function validateAndPreview(file) {
  if (!file.type.startsWith("image/")) {
    showToast("File harus berupa gambar.", "err");
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    showToast("Ukuran file melebihi 5MB.", "err");
    return;
  }
  showPreview(file);
  scanStatus.textContent = `${file.name} siap dideteksi.`;
}

uploadBtn.addEventListener("click", () => {
  const file = fileInput.files[0];
  if (!file) {
    scanStatus.textContent = "Pilih file gambar terlebih dahulu.";
    showToast("Pilih file gambar dulu.", "err");
    return;
  }
  sendImage(file, file.name);
});

sampleBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/static/img/sample_leaf.jpg");
    const blob = await res.blob();
    showPreview(blob);
    scanStatus.textContent = "Contoh citra dimuat. Menjalankan deteksi...";
    sendImage(blob, "sample_leaf.jpg");
  } catch {
    showToast("Gagal memuat contoh gambar.", "err");
  }
});

/* ---------------- Prediction ---------------- */
function setLoading(loading) {
  uploadBtn.disabled = loading;
  sampleBtn.disabled = loading;
  previewWrap.classList.toggle("analyzing", loading);
  if (loading) {
    scanStatus.textContent = "Menganalisis citra... mohon tunggu.";
    scanStatus.style.color = "var(--secondary)";
  } else {
    scanStatus.style.color = "";
    if (scanStatus.textContent.startsWith("Menganalisis")) scanStatus.textContent = "";
  }
}

async function sendImage(blob, name) {
  if (blob.size > 5 * 1024 * 1024) {
    showToast("Ukuran file melebihi 5MB.", "err");
    return;
  }
  setLoading(true);
  const form = new FormData();
  form.append("image", blob, name);
  try {
    const res = await fetch("/predict", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok || data.status !== "success") {
      throw new Error(data.message || `HTTP ${res.status}`);
    }
    resultSource = "scan";
    renderResult(data);
    loadHistory();
  } catch (err) {
    scanStatus.textContent = "Gagal: " + (err.message || "terjadi kesalahan");
    showToast("Gagal menganalisis gambar.", "err");
  } finally {
    setLoading(false);
  }
}

/* ---------------- Render result ---------------- */
function renderResult(data) {
  currentResult = data;
  const info = data.info || {};
  const analysis = data.analysis || {};
  const quality = analysis.quality || {};

  resCategory.textContent = info.category || "Klasifikasi Patogen";
  resDisease.textContent = data.display_disease || data.disease || "-";
  resLatin.textContent = info.latin || "-";

  const tone = (data.severity && data.severity.tone) || "moderate";
  severityBadge.className = "status-chip " + tone;
  severityText.textContent =
    `Keparahan: ${(data.severity && data.severity.label) || "-"} (${(data.severity && data.severity.stage) || "-"})`;

  const conf = Number(data.confidence || 0);
  resConfidence.textContent = conf.toFixed(1);
  gaugeText.textContent = conf.toFixed(1) + "%";
  gaugeProgress.setAttribute("stroke-dasharray", `${conf}, 100`);
  resConfLabel.textContent = data.confidence_label || "";
  const count = analysis.box_count || 0;
  resConfNote.textContent =
    count > 0
      ? `${info.confidence_note || ""} Terdeteksi ${count} area lesi pada citra.`
      : info.confidence_note || "";

  impactTitle.textContent = info.impact_title || "Dampak terhadap Akumulasi Glukomanan:";
  impactText.innerHTML = info.impact || "-";

  metricGrid.innerHTML = (info.metrics || [])
    .map(
      (m) => `
      <div class="metric">
        <span class="metric-label">${escapeHtml(m.label)}</span>
        <span class="metric-value ${escapeHtml(m.tone || "")}">${escapeHtml(m.value)}</span>
        <span class="metric-note">${escapeHtml(m.note)}</span>
      </div>`
    )
    .join("");

  tabPanelGejala.innerHTML = `
    <div class="detail-grid">${(info.symptoms || []).map(infoCard).join("")}</div>`;
  tabPanelRekomendasi.innerHTML = `
    <div class="detail-grid">${(info.recommendations || []).map(recCard).join("")}</div>`;
  tabPanelPencegahan.innerHTML = `
    <div class="detail-grid">${(info.prevention || []).map(infoCard).join("")}</div>`;
  setTab("gejala");

  // Image & overlay
  resultImage.src = data.image.url;
  heatmapLayer.hidden = true;
  heatmapLayer.src = analysis.heatmap || "";
  toggleHeatmap.classList.remove("active");
  toggleHeatmap.setAttribute("aria-pressed", "false");
  toggleHeatmap.disabled = !analysis.heatmap;
  heatmapIcon.textContent = "layers";

  bboxVisible = true;
  bboxLayer.style.display = "block";
  toggleBbox.classList.add("active");
  toggleBbox.setAttribute("aria-pressed", "true");
  bboxIcon.textContent = "check_box";
  buildBoxes(analysis.boxes || []);

  viewerEmpty.hidden = true;
  imageFrame.hidden = false;
  imageFrame.style.setProperty("--ar", `${data.image.width} / ${data.image.height}`);
  zoom = 1;
  applyZoom();

  metaRes.textContent = data.image.resolution;
  metaArea.textContent = `${analysis.lesion_area ?? 0}% Helaian Daun`;
  metaQuality.textContent = `${quality.focus || "-"} \u00b7 ${quality.exposure || "-"}`;
  inferenceBadge.textContent = count > 0 ? `${count} area lesi` : "Tanpa lesi";
  reticle.textContent = `${data.model || "EfficientNetB0"} \u00b7 ${data.image.width}\u00d7${data.image.height} px`;

  // Sub header
  breadcrumb.innerHTML = `
    <span>Beranda</span>
    <span class="material-symbols-outlined">chevron_right</span>
    <span>Analisis Citra AI</span>
    <span class="material-symbols-outlined">chevron_right</span>
    <span>${escapeHtml(data.diagnosis_id)}</span>
    <span class="material-symbols-outlined">chevron_right</span>
    <span class="current">Hasil Analisis</span>`;
  pageTitle.textContent = "Laporan Hasil Diagnosis Patologi AI";
  pageBadge.textContent = "ID: " + data.diagnosis_id;
  const qualityTone = quality.tone === "optimal" ? "ok" : quality.tone === "critical" ? "warn" : "";
  telemetryStrip.innerHTML = `
    <div class="chip"><span class="material-symbols-outlined">calendar_today</span><span>${escapeHtml(data.time)}</span></div>
    <div class="chip ${qualityTone}"><span class="material-symbols-outlined">lens_blur</span><span>${escapeHtml(quality.focus || "-")} &middot; ${escapeHtml(quality.exposure || "-")}</span></div>
    <div class="chip"><span class="material-symbols-outlined">memory</span><span>${escapeHtml(data.model)}</span></div>`;

  // Bottom bar
  $("saveText").textContent = `Diagnosis ${data.diagnosis_id} \u00b7 Tersimpan di Riwayat Lokal`;
  $("saveSub").textContent = `Tersimpan ${data.time} \u00b7 ${data.model}`;

  scanView.hidden = true;
  historyView.hidden = true;
  resultView.hidden = false;
  bottomBar.hidden = false;
  resultBack.hidden = resultSource !== "history";
  setNav("scan");
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Fit after layout & when image is ready
  requestAnimationFrame(fitImageFrame);
  resultImage.onload = fitImageFrame;
}

function infoCard(item) {
  const noteExtra = item.note_tone === "moderate" ? " moderate" : "";
  return `
    <article class="info-card">
      <div class="info-card-head">
        <span class="material-symbols-outlined">${escapeHtml(item.icon || "eco")}</span>
        <h3>${escapeHtml(item.title)}</h3>
      </div>
      <p>${item.text || ""}</p>
      ${item.note ? `<div class="info-note${noteExtra}">${escapeHtml(item.note)}</div>` : ""}
    </article>`;
}

function recCard(item) {
  const details = (item.details || [])
    .map(
      (d) => `<div class="rec-row"><span>${escapeHtml(d.label)}</span><strong>${escapeHtml(d.value)}</strong></div>`
    )
    .join("");
  const tone = item.tone || "neutral";
  return `
    <article class="rec-card ${tone}">
      <div class="rec-top">
        <span class="rec-tag">${escapeHtml(item.tag)}</span>
        <span class="material-symbols-outlined">${escapeHtml(item.icon || "science")}</span>
      </div>
      <h3>${escapeHtml(item.title)}</h3>
      <p>${item.text || ""}</p>
      <div class="rec-details">${details}</div>
      ${item.footnote ? `<p class="rec-foot">${escapeHtml(item.footnote)}</p>` : ""}
    </article>`;
}

function buildBoxes(boxes) {
  bboxLayer.innerHTML = boxes
    .map(
      (b) => `
      <div class="bbox" style="left:${b.x}%;top:${b.y}%;width:${b.w}%;height:${b.h}%">
        <span class="bbox-label">${escapeHtml(b.label)} &middot; ${b.area_pct}%</span>
      </div>`
    )
    .join("");
}

function fitImageFrame() {
  if (!currentResult || imageFrame.hidden) return;
  const stage = viewerStage.getBoundingClientRect();
  if (!stage.width) return;
  const ratio = currentResult.image.width / currentResult.image.height;
  const isMobile = window.innerWidth <= 760;
  const inFullscreen = Boolean(document.fullscreenElement);
  const maxHeight =
    isMobile && !inFullscreen ? window.innerHeight * 0.55 : stage.height * 0.98;
  let width = stage.width * 0.99;
  let height = width / ratio;
  if (height > maxHeight) {
    height = maxHeight;
    width = height * ratio;
  }
  width = Math.max(120, width);
  height = Math.max(120, height);
  imageFrame.style.width = `${width}px`;
  imageFrame.style.height = `${height}px`;
  // Di mobile, rapatkan stage agar tidak menyisakan ruang hitam besar.
  viewerStage.style.height =
    isMobile && !inFullscreen ? `${Math.round(height + 16)}px` : "";
}

window.addEventListener("resize", fitImageFrame);

/* ---------------- Viewer controls ---------------- */
function applyZoom() {
  imageFrame.style.transform = `scale(${zoom})`;
}
$("zoomIn").addEventListener("click", () => {
  zoom = Math.min(2.5, zoom + 0.25);
  applyZoom();
});
$("zoomOut").addEventListener("click", () => {
  zoom = Math.max(1, zoom - 0.25);
  applyZoom();
});
$("fullscreenBtn").addEventListener("click", () => {
  const card = document.querySelector(".viewer-card");
  if (!document.fullscreenElement) {
    card.requestFullscreen?.().catch(() => showToast("Layar penuh tidak didukung.", "err"));
  } else {
    document.exitFullscreen?.();
  }
});
document.addEventListener("fullscreenchange", () => setTimeout(fitImageFrame, 60));

toggleBbox.addEventListener("click", () => {
  bboxVisible = !bboxVisible;
  bboxLayer.style.display = bboxVisible ? "block" : "none";
  toggleBbox.classList.toggle("active", bboxVisible);
  toggleBbox.setAttribute("aria-pressed", String(bboxVisible));
  bboxIcon.textContent = bboxVisible ? "check_box" : "check_box_outline_blank";
});

toggleHeatmap.addEventListener("click", () => {
  const show = heatmapLayer.hidden;
  heatmapLayer.hidden = !show;
  toggleHeatmap.classList.toggle("active", show);
  toggleHeatmap.setAttribute("aria-pressed", String(show));
  heatmapIcon.textContent = show ? "layers" : "layers_clear";
});

/* ---------------- Tabs ---------------- */
const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");

function setTab(name) {
  tabButtons.forEach((b) => {
    const active = b.dataset.tab === name;
    b.classList.toggle("active", active);
    b.setAttribute("aria-selected", active ? "true" : "false");
  });
  tabPanels.forEach((p) => {
    p.hidden = p.dataset.panel !== name;
  });
}
tabButtons.forEach((b) => b.addEventListener("click", () => setTab(b.dataset.tab)));

$("openProtocol").addEventListener("click", () => {
  setTab("rekomendasi");
  document.querySelector(".tabs-card").scrollIntoView({ behavior: "smooth", block: "start" });
});

/* ---------------- Bottom actions ---------------- */
$("downloadPdf").addEventListener("click", () => {
  showToast("Membuka dialog cetak. Pilih 'Save as PDF'.", "info");
  setTimeout(() => window.print(), 250);
});

$("shareBtn").addEventListener("click", async () => {
  if (!currentResult) return;
  const d = currentResult;
  const text =
    `Diagnosis PorangAI ${d.diagnosis_id}: ${d.display_disease} ` +
    `(${d.confidence}% keyakinan, keparahan ${d.severity.label}).`;
  try {
    if (navigator.share) {
      await navigator.share({ title: "PorangAI Precision Agro", text, url: location.href });
    } else {
      await navigator.clipboard.writeText(`${text} ${location.href}`);
      showToast("Ringkasan diagnosis disalin ke clipboard.", "ok");
    }
  } catch {
    showToast("Berbagi dibatalkan.", "info");
  }
});

/* ---------------- History ---------------- */
async function loadHistory() {
  historyList.innerHTML = "<em>Memuat riwayat...</em>";
  try {
    const res = await fetch("/api/riwayat?limit=10");
    const data = await res.json();
    if (data.status !== "success") throw new Error("Gagal memuat");
    if (!data.data.length) {
      historyList.innerHTML = "<em>Belum ada riwayat prediksi. Mulai deteksi pertama Anda.</em>";
      return;
    }
    historyList.innerHTML = data.data.map(historyRow).join("");
    historyList.querySelectorAll("[data-history]").forEach((row) => {
      row.addEventListener("click", () => openHistoryDetail(row.dataset.history));
    });
  } catch {
    historyList.innerHTML = "<em>Gagal memuat riwayat.</em>";
  }
}

function historyRow(item) {
  const sev = item.severity || "";
  const tone =
    sev === "Berat" ? "critical"
      : sev === "Sedang" ? "moderate"
        : sev === "Ringan" || sev === "Sehat" ? "optimal"
          : "neutral";
  const thumb = item.image_url
    ? `<img class="history-thumb" src="${escapeHtml(item.image_url)}" alt="" loading="lazy" />`
    : `<div class="history-thumb"></div>`;
  return `
    <button class="history-row" data-history="${escapeHtml(item.diagnosis_id || "")}" type="button">
      ${thumb}
      <span class="history-name">
        <strong>${escapeHtml(item.hasil_prediksi)}</strong>
        <small>${escapeHtml(item.diagnosis_id || "-")} &middot; ${escapeHtml(item.model || "")}</small>
      </span>
      <span class="status-chip ${tone}">${escapeHtml(sev || "—")}</span>
      <span class="history-conf">${Number(item.confidence || 0).toFixed(1)}%</span>
      <span class="history-time">${escapeHtml(historyTime(item))}</span>
    </button>`;
}

function historyTime(item) {
  if (item.waktu_lokal) return item.waktu_lokal;
  if (!item.waktu) return "";
  const d = new Date(item.waktu.replace(" ", "T") + "Z");
  if (Number.isNaN(d.getTime())) return item.waktu;
  return `${d.getDate()} ${MONTHS_ID[d.getMonth()]} ${d.getFullYear()}, ${pad(d.getHours())}:${pad(d.getMinutes())} WIB`;
}

async function openHistoryDetail(id) {
  if (!id) return;
  resultSource = "history";
  try {
    const res = await fetch(`/api/riwayat/${encodeURIComponent(id)}`);
    const data = await res.json();
    if (!res.ok || data.status !== "success") throw new Error(data.message || "Tidak ditemukan");
    renderResult(data);
    showToast("Memuat riwayat " + id, "ok");
  } catch {
    showToast("Riwayat tidak dapat dimuat.", "err");
  }
}

backToHistory.addEventListener("click", showHistory);

/* ---------------- Modals ---------------- */
function openModal(el) {
  lastFocused = document.activeElement;
  el.hidden = false;
  document.body.style.overflow = "hidden";
  const closer = el.querySelector("[data-close]");
  if (closer) closer.focus();
}
function closeModal(el) {
  el.hidden = true;
  document.body.style.overflow = "";
  if (lastFocused) lastFocused.focus();
}
document.querySelectorAll("[data-close]").forEach((btn) => {
  btn.addEventListener("click", () => closeModal($(btn.dataset.close)));
});
[guideModal, helpModal].forEach((modal) => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal(modal);
  });
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  [guideModal, helpModal].forEach((m) => {
    if (!m.hidden) closeModal(m);
  });
});

/* ---------------- Init ---------------- */
scanHeader();
loadHistory();

fetch("/health")
  .then((r) => r.json())
  .then((h) => {
    const pill = document.querySelector(".model-pill");
    if (!pill || h.trained) return;
    pill.innerHTML =
      '<span class="dot-pulse" style="background:#ba1a1a"></span>' +
      "<span>Model:</span><strong style=\"color:#ba1a1a\">Tidak tersedia</strong>";
    showToast("File model tidak ditemukan di folder models/.", "err");
  })
  .catch(() => {});
