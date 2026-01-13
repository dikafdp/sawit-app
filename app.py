import streamlit as st
from ultralytics import YOLO
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Sistem Cerdas Sawit",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. LOAD ASSETS (ANIMASI & MODEL)
# ---------------------------------------------------------------------
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Animasi "HUD Tech" (Lingkaran digital berputar) tetap dipakai karena keren
lottie_tech = load_lottieurl("https://lottie.host/5a909436-7013-40e9-9d50-ca7eb230554e/R5H4s6M6yX.json")

@st.cache_resource
def load_model():
    return YOLO("best.pt")

# ---------------------------------------------------------------------
# 3. CSS "HIGH-TECH INTERFACE" (Gaya Tetap Modern)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT TEKNIKAL */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* --- BACKGROUND --- */
    .stApp {
        background-color: #020617; /* Hitam Kebiruan Gelap */
        background-image: 
            radial-gradient(circle at 50% 0%, #1e293b 0%, transparent 70%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Rajdhani', sans-serif;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3, p, span, div {
        color: #e2e8f0;
    }

    /* Judul Utama */
    h1 {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 2.2rem;
        background: linear-gradient(to bottom, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    /* Subjudul Kecil (Gaya Terminal) */
    .tech-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #38bdf8; /* Cyan Blue */
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        margin-bottom: 40px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* --- TOMBOL KAMERA --- */
    [data-testid="stCameraInput"] {
        border: 1px solid rgba(56, 189, 248, 0.2);
        background: rgba(15, 23, 42, 0.6);
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
        transform: translateY(-2px);
    }

    /* --- PANEL HASIL --- */
    .tech-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid #38bdf8;
        backdrop-filter: blur(10px);
        padding: 25px;
        margin-top: 30px;
        position: relative;
    }

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
        color: #64748b;
        font-size: 0.8rem;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 5px;
    }
    
    .data-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #f1f5f9;
        display: block;
    }

    .tech-card img {
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    /* Footer Status */
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
    st.error("ERROR SISTEM: File model tidak ditemukan.")
    st.stop()

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    if lottie_tech:
        st_lottie(lottie_tech, height=80, key="tech_anim")
    else:
        st.write("💠")

with col_head2:
    st.markdown("<h1>SISTEM CERDAS SAWIT</h1>", unsafe_allow_html=True)
    st.markdown('<div class="tech-subtitle">/// ANALISIS KEMATANGAN BERBASIS AI ///</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.8rem; color:#64748b;">[ SILAKAN AMBIL FOTO BUAH ]</p>', unsafe_allow_html=True)

# Area Kamera
img_file = st.camera_input("Kamera", label_visibility="hidden")

# --- PROSES & OUTPUT ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Efek Loading Bar ala Terminal
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)
    
    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1] # BGR to RGB
    boxes = results[0].boxes
    
    # --- HASIL TAMPILAN INDONESIA ---
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    
    # Header Kartu
    st.markdown('<span class="data-label">>> HASIL DIAGNOSA</span>', unsafe_allow_html=True)
    
    # Tampilkan Gambar
    st.image(res_plotted, use_container_width=True)
    
    # Data Analisa
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown('<span class="data-label">JUMLAH DETEKSI</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="data-value">{len(boxes)} BUAH</span>', unsafe_allow_html=True)
        
    with col_res2:
        st.markdown('<span class="data-label">STATUS PANEN</span>', unsafe_allow_html=True)
        if len(boxes) > 0:
            st.markdown('<span class="data-value" style="color:#4ade80;">TERIDENTIFIKASI</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="data-value" style="color:#f472b6;">TIDAK JELAS</span>', unsafe_allow_html=True)

    # Footer Teknis (Bahasa Indonesia & Relevan)
    st.markdown(f'''
        <div class="status-bar">
            <span>ID: SWT-{int(time.time())}</span>
            <span>MODEL: YOLOv11-NANO</span>
            <span>MODUL KAMERA: AKTIF</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
