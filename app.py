import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Deteksi Sawit YOLOv11",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. LOAD MODEL
# ---------------------------------------------------------------------
@st.cache_resource
def load_model():
    return YOLO("best.pt")

# ---------------------------------------------------------------------
# 3. CSS: TEMA DARK GRID (TAPI FONT PROFESSIONAL)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT ROBOTO (Standar Akademis & Profesional) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* --- BACKGROUND (TEMA GRID YANG ANDA SUKA) --- */
    .stApp {
        background-color: #020617; /* Hitam Kebiruan Gelap */
        /* Efek Grid Halus tetap dipertahankan karena bagus */
        background-image: 
            radial-gradient(circle at 50% 0%, #1e293b 0%, transparent 70%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Roboto', sans-serif; /* Font Ganti Jadi Normal */
    }

    /* --- TYPOGRAPHY (TEXT) --- */
    h1, h2, h3, p, span, div, label {
        color: #e2e8f0;
    }

    /* JUDUL UTAMA (RATA TENGAH & BERSIH) */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        text-align: center; /* RATA TENGAH */
        margin-bottom: 5px;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* SUBJUDUL (INFORMASI METODE) */
    .subtitle {
        font-family: 'Roboto', sans-serif;
        color: #94a3b8; /* Abu-abu kalem */
        text-align: center;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 40px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 20px;
    }

    /* --- TOMBOL KAMERA (CLEAN STYLE) --- */
    [data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(15, 23, 42, 0.6);
        border-radius: 8px;
    }

    [data-testid="stCameraInput"] button {
        background-color: #2563eb !important; /* Biru Akademis */
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }

    [data-testid="stCameraInput"] button:hover {
        background-color: #1d4ed8 !important;
        transform: translateY(-2px);
    }

    /* --- KARTU HASIL (SIMPLE & ELEGANT) --- */
    .result-card {
        background: rgba(30, 41, 59, 0.5); /* Semi transparan */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
        text-align: center;
    }

    .result-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
        display: block;
        letter-spacing: 0.5px;
    }

    /* Gambar Hasil */
    .result-card img {
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Tabel Info Sederhana */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.95rem;
    }
    .info-label { color: #94a3b8; }
    .info-value { color: #f8fafc; font-weight: 600; }

    /* Footer Text */
    .footer-text {
        text-align: center;
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 30px;
    }

    /* Hapus elemen default Streamlit */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. LOGIKA UTAMA
# ---------------------------------------------------------------------

try:
    model = load_model()
except Exception:
    st.error("Error: File model 'best.pt' tidak ditemukan.")
    st.stop()

# --- HEADER (RATA TENGAH, TANPA LOGO SAMPING) ---
# Tidak pakai kolom lagi, langsung tulis biar center
st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Implementasi Algoritma YOLOv11 untuk Klasifikasi Buah Sawit</p>', unsafe_allow_html=True)

# --- INPUT KAMERA ---
st.markdown('<p style="text-align:center; color:#cbd5e1; margin-bottom:10px;">Silakan ambil foto buah sawit:</p>', unsafe_allow_html=True)
img_file = st.camera_input("Kamera", label_visibility="hidden")

# --- PROSES & OUTPUT ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Loading sederhana
    with st.spinner('Sedang menganalisis citra...'):
        # Deteksi
        results = model(image)
        res_plotted = results[0].plot()[:, :, ::-1] # BGR ke RGB
        boxes = results[0].boxes
    
    # --- TAMPILAN HASIL (BERSIH & RAPI) ---
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<span class="result-header">HASIL ANALISIS</span>', unsafe_allow_html=True)
    
    # Tampilkan Gambar
    st.image(res_plotted, use_container_width=True)
    
    # Informasi (Tabel Rapi)
    st.markdown(f"""
        <div style="margin-top: 20px; text-align: left;">
            <div class="info-row">
                <span class="info-label">Jumlah Terdeteksi</span>
                <span class="info-value">{len(boxes)} Buah</span>
            </div>
            <div class="info-row">
                <span class="info-label">Status Deteksi</span>
                <span class="info-value" style="color: {'#4ade80' if len(boxes) > 0 else '#f87171'};">
                    {'BERHASIL' if len(boxes) > 0 else 'TIDAK ADA OBJEK'}
                </span>
            </div>
            <div class="info-row" style="border-bottom: none;">
                <span class="info-label">Model AI</span>
                <span class="info-value">YOLOv11 Nano</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('<div class="footer-text">Sistem Cerdas Perkebunan © 2024 • Powered by YOLOv11</div>', unsafe_allow_html=True)
