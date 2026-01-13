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
    page_title="Sawit Vision AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. FUNGSI LOAD ASSETS
# ---------------------------------------------------------------------
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

@st.cache_resource
def load_model():
    return YOLO("best.pt")

# Animasi 'Scanning' yang lebih abstrak & elegan (bukan kartun drone)
lottie_scan = load_lottieurl("https://lottie.host/9c33d077-7670-4cc7-b765-b34e40237731/8q1Yg7Zt6k.json")

# ---------------------------------------------------------------------
# 3. CSS: MODERN ELEGANT THEME (Deep Slate & Emerald)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* Import Font Inter (Standar Desain Modern) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* --- RESET BACKGROUND --- */
    .stApp {
        background-color: #0f172a; /* Deep Slate (Gelap Elegan) */
        font-family: 'Inter', sans-serif;
    }

    /* Warna Teks Umum */
    h1, h2, h3, p, span, div {
        color: #e2e8f0;
    }

    /* --- HEADER STYLING --- */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        color: #64748b !important; /* Abu-abu muted */
        font-size: 1rem;
        font-weight: 400;
        margin-top: -10px;
    }

    /* --- TOMBOL KAMERA (MINIMALIS) --- */
    [data-testid="stCameraInput"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
    }
    
    /* Tombol Take Photo */
    [data-testid="stCameraInput"] button {
        background-color: #10b981 !important; /* Emerald Green Matte */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stCameraInput"] button:hover {
        background-color: #059669 !important; /* Gelap sedikit saat hover */
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    /* --- HASIL CARD (ELEGANT GLASS) --- */
    .result-card {
        background: rgba(30, 41, 59, 0.7); /* Slate transparan */
        backdrop-filter: blur(12px);       /* Blur halus */
        border: 1px solid rgba(255, 255, 255, 0.08); /* Border tipis halus */
        border-radius: 16px;
        padding: 24px;
        margin-top: 30px;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.8s ease-out;
    }

    .result-title {
        text-transform: uppercase;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: #94a3b8; /* Text muted */
        margin-bottom: 20px;
        display: block;
    }

    /* Gambar Hasil */
    .result-card img {
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* --- BADGE STATUS (CLEAN PILL) --- */
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 16px;
        margin-top: 20px;
        border-radius: 999px; /* Pill shape */
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .pill-success {
        background: rgba(16, 185, 129, 0.15); /* Hijau transparan lembut */
        color: #34d399; /* Teks Hijau soft */
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .pill-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }

    /* Animasi Halus */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. LOGIKA APLIKASI
# ---------------------------------------------------------------------

# --- HEADER SECTION ---
col1, col2 = st.columns([1, 4])

with col1:
    # Animasi Scanning Icon (Kecil dan rapi di pojok)
    if lottie_scan:
        st_lottie(lottie_scan, height=70, key="scan_icon")
    else:
        st.write("🔬")

with col2:
    st.markdown("<h1>Sawit Quality Analysis</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Maturity Detection System</p>', unsafe_allow_html=True)

st.write("") # Spacer

# --- LOAD MODEL ---
# Loading state yang bersih (tanpa spinner raksasa)
try:
    model = load_model()
except Exception:
    st.error("Model 'best.pt' not detected.")
    st.stop()

# --- MAIN CAMERA AREA ---
img_file = st.camera_input("Input", label_visibility="hidden")

if img_file is not None:
    image = Image.open(img_file)
    
    # Progress bar minimalis sebagai pengganti spinner
    progress_text = "Analyzing image structure..."
    my_bar = st.progress(0, text=progress_text)

    # Simulasi loading sebentar (biar terasa prosesnya)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty() # Hilangkan bar setelah selesai

    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    boxes = results[0].boxes
    
    # --- TAMPILAN HASIL (ELEGANT CARD) ---
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<span class="result-title">Detection Result</span>', unsafe_allow_html=True)
    
    st.image(res_plotted, use_container_width=True)
    
    # Badge Logic
    if len(boxes) > 0:
        st.markdown(f'''
            <div class="status-pill pill-success">
                <span>✓ {len(boxes)} Palm Bunches Detected</span>
            </div>
        ''', unsafe_allow_html=True)
        
        # (Opsional) Tampilkan detail kelas dengan teks kecil rapi
        names = model.names
        class_list = [names[int(c)] for c in boxes.cls]
        unique_classes = list(set(class_list))
        st.markdown(f'<p style="color:#64748b; font-size:0.8rem; margin-top:10px;">Classification: {", ".join(unique_classes)}</p>', unsafe_allow_html=True)

    else:
        st.markdown('''
            <div class="status-pill pill-warning">
                <span>⚠ No objects identified</span>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
