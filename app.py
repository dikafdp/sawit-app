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
    page_title="Sawit AI - Premium Detection",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. FUNGSI LOAD ANIMASI & MODEL
# ---------------------------------------------------------------------
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Load Animasi: "Scanning Radar" (Modern & Techy)
lottie_radar = load_lottieurl("https://lottie.host/9c33d077-7670-4cc7-b765-b34e40237731/8q1Yg7Zt6k.json")

@st.cache_resource
def load_model():
    return YOLO("best.pt")

# ---------------------------------------------------------------------
# 3. CSS MODERN DARK MODE (GAYA REFERENSI ANDA)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT MODERN (INTER) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* RESET DEFAULT STREAMLIT */
    .stApp {
        background-color: #0E0E10 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* WARNA TEKS DEFAULT */
    h1, h2, h3, p, div, span, label {
        color: #FFFFFF !important;
    }

    /* JUDUL UTAMA */
    h1 {
        font-weight: 800 !important;
        text-align: left; /* Rata kiri biar pas sama animasi */
        margin-bottom: 0.2rem;
        background: linear-gradient(to right, #ffffff, #a8a8a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        padding-top: 10px;
    }

    /* SUBJUDUL */
    .sub-header {
        text-align: left;
        color: #8A8F98 !important;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* CUSTOM TOMBOL KAMERA */
    [data-testid="stCameraInput"] {
        border: 1px solid #2D3339;
        background-color: #1C1C21;
        border-radius: 16px;
        padding: 10px;
    }

    [data-testid="stCameraInput"] button {
        background-color: #FFFFFF !important;
        color: #0E0E10 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stCameraInput"] button:hover {
        background-color: #E1E1E1 !important;
        transform: scale(1.02);
    }

    /* KOTAK HASIL (PREMIUM CARD) */
    .hasil-card {
        background-color: #1C1C21;
        border: 1px solid #2D3339;
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        margin-top: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        animation: fadeUp 0.6s ease-out;
    }

    .hasil-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #8A8F98 !important;
        margin-bottom: 20px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .hasil-card img {
        border-radius: 16px;
        border: 1px solid #2D3339;
    }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* BADGES */
    .stat-badge-success {
        display: inline-block;
        background: rgba(46, 204, 113, 0.15);
        color: #2ecc71 !important;
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 20px;
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    
    .stat-badge-warning {
        display: inline-block;
        background: rgba(241, 196, 15, 0.15);
        color: #f1c40f !important;
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 20px;
        border: 1px solid rgba(241, 196, 15, 0.3);
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. LOGIKA APLIKASI
# ---------------------------------------------------------------------

try:
    model = load_model()
except Exception:
    st.error("⚠️ File model 'best.pt' tidak ditemukan.")
    st.stop()

# --- HEADER AREA (DENGAN ANIMASI) ---
# Kita bagi header jadi 2 kolom: Animasi (Kecil) + Teks (Besar)
col_anim, col_text = st.columns([1, 4])

with col_anim:
    # Tampilkan animasi radar/scan
    if lottie_radar:
        st_lottie(lottie_radar, height=80, key="radar_anim")
    else:
        st.write("✨") # Fallback jika animasi gagal load

with col_text:
    st.title("Sawit AI")
    st.markdown('<p class="sub-header">Advanced Computer Vision for Palm Oil Maturity Detection</p>', unsafe_allow_html=True)

st.write("") # Jarak kosong

# --- AREA KAMERA ---
col_spacer1, col_cam, col_spacer2 = st.columns([1, 4, 1])

with col_cam:
    img_file = st.camera_input("Label Tersembunyi", label_visibility="hidden")

# --- PROSES & HASIL ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Progress Bar sebagai pengganti spinner biasa (Biar lebih keren)
    progress_text = "Analyzing image structure..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01) # Simulasi loading cepat
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    
    # --- TAMPILAN HASIL (CARD) ---
    st.markdown('<div class="hasil-card">', unsafe_allow_html=True)
    st.markdown('<span class="hasil-label">Analysis Results</span>', unsafe_allow_html=True)
    
    st.image(res_plotted, use_container_width=True)
    
    boxes = results[0].boxes
    if len(boxes) > 0:
        st.markdown(f'<div class="stat-badge-success">✨ {len(boxes)} Objects Detected Successfully</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="stat-badge-warning">⚠️ No Objects Detected</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
