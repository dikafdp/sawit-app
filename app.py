import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Deteksi Sawit YOLOv11",
    page_icon="🥥",
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
# 3. CSS: HIGH-TECH STYLE (VISUAL TETAP KEREN) TAPI RAPI
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* KEMBALIKAN FONT KEREN (Rajdhani & Share Tech Mono) */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* BACKGROUND GRID (YANG ANDA SUKA) */
    .stApp {
        background-color: #020617; /* Hitam Kebiruan Gelap */
        background-image: 
            radial-gradient(circle at 50% 0%, #1e293b 0%, transparent 70%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Rajdhani', sans-serif;
    }

    /* TYPOGRAPHY */
    h1, h2, h3, p, span, div, label {
        color: #e2e8f0;
    }

    /* JUDUL UTAMA (RATA TENGAH & AKADEMIS) */
    h1 {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 2.2rem;
        background: linear-gradient(to bottom, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; /* SUDAH DITENGAHKAN */
        margin-bottom: 0;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        padding-top: 20px;
    }
    
    /* SUBJUDUL (GAYA TERMINAL TAPI ISINYA ILMIAH) */
    .tech-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #38bdf8; /* Cyan Blue */
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        margin-bottom: 30px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* TOMBOL KAMERA (GAYA TECH) */
    [data-testid="stCameraInput"] {
        border: 1px solid rgba(56, 189, 248, 0.3);
        background: rgba(15, 23, 42, 0.8);
        border-radius: 4px;
    }

    [data-testid="stCameraInput"] button {
        background-color: transparent !important;
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
        font-family: 'Share Tech Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        border-radius: 2px !important;
    }

    [data-testid="stCameraInput"] button:hover {
        background-color: rgba(56, 189, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }

    /* PANEL HASIL (GLASS TECH) */
    .tech-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid #38bdf8;
        backdrop-filter: blur(10px);
        padding: 25px;
        margin-top: 30px;
        position: relative;
    }

    /* Hiasan Siku Pojok Kanan Atas */
    .tech-card::before {
        content: "";
        position: absolute;
        top: -1px; right: -1px;
        width: 20px; height: 20px;
        border-top: 1px solid #38bdf8;
        border-right: 1px solid #38bdf8;
    }

    .data-label {
        font-family: 'Share Tech Mono', monospace;
        color: #94a3b8; /* Abu-abu */
        font-size: 0.8rem;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 5px;
    }
    
    .data-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        display: block;
    }

    .tech-card img {
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    /* Footer Status Akademis */
    .status-bar {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 10px;
        margin-top: 10px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #38bdf8;
    }

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
    st.error("Error: Model weights not found.")
    st.stop()

# --- HEADER (TANPA LOGO, HANYA TEKS TENGAH) ---
st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<div class="tech-subtitle">/// IMPLEMENTASI ALGORITMA YOLOv11 ///</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.8rem; color:#94a3b8;">[ SILAKAN AMBIL CITRA BUAH ]</p>', unsafe_allow_html=True)

img_file = st.camera_input("Kamera", label_visibility="hidden")

# --- PROSES & OUTPUT ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Progress bar (Visual Proses)
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)
    
    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1] # BGR to RGB
    boxes = results[0].boxes
    
    # --- HASIL (BAHASA AKADEMIS) ---
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    
    # Header Kartu
    st.markdown('<span class="data-label">>> HASIL ANALISIS CITRA</span>', unsafe_allow_html=True)
    
    # Tampilkan Gambar
    st.image(res_plotted, use_container_width=True)
    
    # Data Analisa
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown('<span class="data-label">JUMLAH OBJEK</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="data-value">{len(boxes)} UNIT</span>', unsafe_allow_html=True)
        
    with col_res2:
        st.markdown('<span class="data-label">KLASIFIKASI</span>', unsafe_allow_html=True)
        if len(boxes) > 0:
            st.markdown('<span class="data-value" style="color:#4ade80;">TERDETEKSI</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="data-value" style="color:#f472b6;">TIDAK JELAS</span>', unsafe_allow_html=True)

    # Footer Teknis (Info Akademis)
    st.markdown(f'''
        <div class="status-bar">
            <span>METODE: YOLOv11</span>
            <span>FRAMEWORK: PYTORCH</span>
            <span>MODUL: COMPUTER VISION</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
