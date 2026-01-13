import streamlit as st
from ultralytics import YOLO
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN (WAJIB DI PALING ATAS)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Neon Sawit AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. FUNGSI LOADER (Animasi & Model)
# ---------------------------------------------------------------------
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

@st.cache_resource
def load_model():
    # Beri jeda sedikit biar animasi loading terasa dramatis
    time.sleep(1.5) 
    return YOLO("best.pt")

# Muat aset di awal
lottie_cyber_drone = load_lottieurl("https://lottie.host/4b6e8f49-5c4d-4519-95ba-2747124d4b2d/3Y6q4uM9y0.json")

# ---------------------------------------------------------------------
# 3. CSS CYBERPUNK TOTAL (ANIMATED & NEON)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* --- IMPORT FONT FUTURISTIK --- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400&display=swap');

    /* --- BACKGROUND ANIMASI BERGERAK (Kunci "Keren") --- */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .stApp {
        /* Gradasi warna gelap neon: Biru Tua -> Ungu -> Hijau Teal */
        background: linear-gradient(-45deg, #0a0f1f, #1a1a2e, #0f3030, #0a0f1f);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite; /* Bergerak terus menerus */
        font-family: 'Roboto', sans-serif !important;
        color: #e0e0e0;
    }

    /* --- JUDUL NEON --- */
    @keyframes flicker {
      0%, 18%, 22%, 25%, 53%, 57%, 100% {
          text-shadow:
          0 0 4px #fff,
          0 0 11px #fff,
          0 0 19px #fff,
          0 0 40px #0fa,
          0 0 80px #0fa,
          0 0 90px #0fa,
          0 0 100px #0fa,
          0 0 150px #0fa;
      }
      20%, 24%, 55% {        
          text-shadow: none;
      }    
    }

    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        color: #fff;
        text-align: center;
        /* Efek kedip neon */
        animation: flicker 3s infinite alternate;     
    }

    /* --- CUSTOM TOMBOL KAMERA (KOTAK CYBER) --- */
    [data-testid="stCameraInput"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stCameraInput"]:hover {
         border: 1px solid rgba(0, 255, 255, 0.8);
         box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
    }

    /* Tombol 'Take Photo' di dalamnya */
    [data-testid="stCameraInput"] button {
        background: linear-gradient(90deg, #00f260, #0575e6) !important; /* Gradasi Hijau-Biru Elektrik */
        border: none !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        letter-spacing: 2px;
        border-radius: 4px !important; /* Sudut tajam futuristik */
        padding: 15px 30px !important;
        transition: all 0.4s ease !important;
        clip-path: polygon(10% 0%, 100% 0, 100% 70%, 90% 100%, 0 100%, 0% 30%); /* Bentuk Cyberpunk */
    }

    [data-testid="stCameraInput"] button:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 10px 30px rgba(5, 117, 230, 0.7) !important;
        background: linear-gradient(90deg, #0575e6, #00f260) !important;
    }

    /* --- KARTU HASIL (GLASSMORPHISM NEON) --- */
    /* Animasi Masuk yang Bouncy (Membal) */
    @keyframes bounceInUp {
      from, 60%, 75%, 90%, to { animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1); }
      from { opacity: 0; transform: translate3d(0, 100px, 0); }
      60% { opacity: 1; transform: translate3d(0, -15px, 0); }
      75% { transform: translate3d(0, 5px, 0); }
      90% { transform: translate3d(0, -2px, 0); }
      to { transform: translate3d(0, 0, 0); }
    }

    .cyber-card {
        background: rgba(23, 23, 35, 0.7); /* Gelap transparan */
        backdrop-filter: blur(20px); /* Efek kaca buram kuat */
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 2px solid transparent;
        /* Border gradasi neon */
        background-image: linear-gradient(rgba(23, 23, 35, 0.7), rgba(23, 23, 35, 0.7)), 
                          linear-gradient(135deg, #00ff87, #60efff);
        background-origin: border-box;
        background-clip: content-box, border-box;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 30px rgba(96, 239, 255, 0.2);
        padding: 30px;
        text-align: center;
        margin-top: 30px;
        /* Terapkan animasi masuk */
        animation: bounceInUp 1s both;
    }

    .cyber-card-title {
        font-family: 'Orbitron', sans-serif;
        color: #60efff; /* Biru Neon */
        font-size: 1.4rem;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .cyber-card img {
        border-radius: 16px;
        border: 2px solid #00ff87; /* Garis hijau neon di gambar */
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.3);
    }

    /* Badge Hasil Neon */
    .neon-badge {
        display: inline-block;
        padding: 10px 25px;
        margin-top: 25px;
        border-radius: 50px;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 0 20px currentColor;
    }

    /* Hapus elemen mengganggu */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. LOGIKA APLIKASI (DENGAN WRAPPER HTML BARU)
# ---------------------------------------------------------------------

# --- HEADER ANIMASI ---
col_anim, col_title = st.columns([1, 3])
with col_anim:
    if lottie_cyber_drone:
        # Animasi drone di kiri
        st_lottie(lottie_cyber_drone, height=130, key="drone")
    else:
        st.write("🛸")
with col_title:
    # Judul dengan efek kedip neon di CSS
    st.markdown("<h1>CYBER PALM DETECT</h1>", unsafe_allow_html=True)
    st.write("AI Powered Agricultural Scanner. System Online.")

st.markdown("---")

# --- LOAD MODEL (DENGAN EFEK SPINNER KEREN) ---
with st.spinner('⚡ Initializing Neural Network...'):
    try:
        model = load_model()
    except Exception:
        st.error("⚠️ SYSTEM FAILURE: Model 'best.pt' not found.")
        st.stop()

# --- KAMERA ---
st.write("### 💠 Activate Scanner")
img_file = st.camera_input("Label Hidden", label_visibility="hidden")

if img_file is not None:
    image = Image.open(img_file)
    
    # Spinner saat proses
    with st.spinner('🔄 Processing Data Stream...'):
        results = model(image)
        res_plotted = results[0].plot()[:, :, ::-1]
        boxes = results[0].boxes
        
        # --- TAMPILAN HASIL (KARTU CYBERPUNK) ---
        # Kita bungkus dengan div class 'cyber-card'
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<div class="cyber-card-title">Scan Analysis Result</div>', unsafe_allow_html=True)
        
        st.image(res_plotted, use_container_width=True)
        
        # Badge Hasil Neon
        if len(boxes) > 0:
             # Warna Hijau Neon untuk sukses
             st.markdown(f'<div class="neon-badge" style="color: #00ff87; border: 2px solid #00ff87;">✅ OBJECTS DETECTED: {len(boxes)}</div>', unsafe_allow_html=True)
        else:
             # Warna Merah Neon untuk gagal
             st.markdown('<div class="neon-badge" style="color: #ff0055; border: 2px solid #ff0055;">⚠️ NO TARGET ACQUIRED</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
