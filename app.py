import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Sistem Deteksi Sawit",
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
# 3. CSS: HIGH-TECH GRID + COMBINED TABLE
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT (Rajdhani & Share Tech Mono) */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Share+Tech+Mono&display=swap');

    /* BACKGROUND GRID */
    .stApp {
        background-color: #020617;
        background-image: 
            radial-gradient(circle at 50% 0%, #1e293b 0%, transparent 70%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3, p, span, div, label { color: #e2e8f0; }

    /* JUDUL (RATA TENGAH) */
    h1 {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(to bottom, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 10px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    /* SUBJUDUL */
    .tech-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #38bdf8;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        margin-bottom: 30px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* TOMBOL KAMERA */
    [data-testid="stCameraInput"] {
        border: 1px solid rgba(56, 189, 248, 0.3);
        background: rgba(15, 23, 42, 0.8);
        border-radius: 6px;
    }
    [data-testid="stCameraInput"] button {
        background-color: transparent !important;
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
        font-family: 'Share Tech Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        border-radius: 4px !important;
    }
    [data-testid="stCameraInput"] button:hover {
        background-color: rgba(56, 189, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }

    /* KARTU HASIL UTAMA */
    .tech-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid #38bdf8;
        backdrop-filter: blur(10px);
        padding: 25px;
        margin-top: 30px;
        position: relative;
    }
    
    /* Header Kartu */
    .data-header {
        font-family: 'Share Tech Mono', monospace;
        color: #94a3b8;
        font-size: 0.85rem;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }

    /* --- STYLE TABEL RAPI (GABUNGAN) --- */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2); /* Garis Cyan Tipis */
        font-size: 1rem;
    }
    
    .info-label { 
        font-family: 'Share Tech Mono', monospace; 
        color: #94a3b8; /* Warna Label Abu */
    }
    
    .info-value { 
        font-family: 'Rajdhani', sans-serif; 
        color: #f1f5f9; /* Warna Value Putih Terang */
        font-weight: 700;
        font-size: 1.1rem;
        text-align: right;
    }

    /* --- STYLE FOOTER STATUS BAR (GABUNGAN) --- */
    .status-bar {
        display: flex;
        justify-content: space-between;
        background: rgba(255,255,255,0.03); /* Sedikit background beda */
        border-top: 1px solid rgba(255,255,255,0.1);
        padding: 10px 15px;
        margin-top: 25px;
        border-radius: 4px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #38bdf8; /* Warna Cyan */
        letter-spacing: 0.5px;
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
    st.error("Error: File model 'best.pt' tidak ditemukan.")
    st.stop()

# --- HEADER ---
st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<div class="tech-subtitle">/// IMPLEMENTASI ALGORITMA DEEP LEARNING YOLOV11 ///</div>', unsafe_allow_html=True)

# --- INPUT ---
st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ SILAKAN AMBIL CITRA BUAH ]</p>', unsafe_allow_html=True)

img_file = st.camera_input("Kamera", label_visibility="hidden")

# --- PROSES ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Visualisasi Loading
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)
    
    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    boxes = results[0].boxes
    
    # --- HASIL GABUNGAN (TABEL + FOOTER) ---
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    st.markdown('<span class="data-header">>> HASIL KLASIFIKASI CITRA</span>', unsafe_allow_html=True)
    
    # Gambar Hasil
    st.image(res_plotted, use_container_width=True)
    
    # 1. TABEL INFORMASI UTAMA (Vertical Rapi)
    st.markdown(f"""
        <div style="margin-top: 20px; text-align: left;">
            
            <div class="info-row">
                <span class="info-label">JUMLAH OBJEK</span>
                <span class="info-value">{len(boxes)} UNIT</span>
            </div>
            
            <div class="info-row">
                <span class="info-label">STATUS DETEKSI</span>
                <span class="info-value" style="color: {'#4ade80' if len(boxes) > 0 else '#f87171'};">
                    {'TERIDENTIFIKASI' if len(boxes) > 0 else 'TIDAK JELAS'}
                </span>
            </div>
            
            <div class="info-row" style="border-bottom: none;">
                <span class="info-label">ARSITEKTUR MODEL</span>
                <span class="info-value">YOLOv11 Nano</span>
            </div>

        </div>
    """, unsafe_allow_html=True)

    # 2. FOOTER TEKNIS (Status Bar di Bawah)
    # Ini memberikan kesan dashboard sistem yang lengkap
    st.markdown(f'''
        <div class="status-bar">
            <span>METODE: YOLOv11</span>
            <span>THRESHOLD: 0.25</span>
            <span>MODUL: CV-PYTORCH</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
