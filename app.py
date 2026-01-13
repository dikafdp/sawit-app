import streamlit as st
from ultralytics import YOLO
from PIL import Image
import requests
from streamlit_lottie import st_lottie

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Sawit Detection AI", 
    page_icon="🌴", 
    layout="centered"
)

# ---------------------------------------------------------------------
# 2. CSS LANGSUNG DI SINI (JURUS ANTI GAGAL)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* Import Font Keren */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Background Utama */
    .stApp {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Judul Aplikasi */
    h1 {
        color: #004d40;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* Subjudul */
    p {
        color: #00695c;
        font-size: 1.1rem;
    }

    /* --- Desain Tombol Kamera --- */
    /* Kita targetkan tombol di dalam elemen kamera */
    button[kind="primary"] {
        background: linear-gradient(45deg, #FF6F00, #FF8F00);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Efek Hover Tombol */
    button[kind="primary"]:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }
    
    /* Tombol Kamera Bawaan Streamlit */
    [data-testid="stCameraInput"] button {
        background-color: #00897b !important;
        color: white !important;
        border-radius: 50px !important;
        border: 2px solid white !important;
    }

    /* --- Kotak Hasil (Card Style) --- */
    .hasil-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #b2dfdb;
        margin-top: 20px;
        animation: slideUp 0.8s ease-out;
    }

    /* Teks Judul Hasil */
    .hasil-label {
        font-size: 1.5rem;
        font-weight: bold;
        color: #004d40;
        margin-bottom: 10px;
        display: block;
    }
    
    /* Animasi Slide Up */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Bersihkan Tampilan */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 3. LOGIKA APLIKASI
# ---------------------------------------------------------------------

# Load Animasi Lottie (Drone/Scan)
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Model
@st.cache_resource
def load_model():
    return YOLO("best.pt")

try:
    model = load_model()
except Exception:
    st.error("Model best.pt tidak ditemukan di GitHub.")

# --- Header ---
col1, col2 = st.columns([1, 2])
with col1:
    # Animasi Petani/Kebun
    lottie_anim = load_lottieurl("https://lottie.host/4b6e8f49-5c4d-4519-95ba-2747124d4b2d/3Y6q4uM9y0.json")
    if lottie_anim:
        st_lottie(lottie_anim, height=150, key="anim")
    else:
        st.write("🌴") # Fallback jika animasi gagal load

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Smart Sawit")
    st.write("Deteksi Kematangan Buah Sawit")

st.markdown("---")

# --- Kamera ---
st.write("### 📸 Ambil Foto")
img_file = st.camera_input("Kamera Label", label_visibility="hidden")

if img_file is not None:
    image = Image.open(img_file)
    
    with st.spinner('Sedang memproses gambar...'):
        results = model(image)
        res_plotted = results[0].plot()[:, :, ::-1]
        
        # --- TAMPILKAN HASIL (HTML WRAPPER) ---
        st.markdown('<div class="hasil-card">', unsafe_allow_html=True)
        st.markdown('<span class="hasil-label">✨ Hasil Analisa ✨</span>', unsafe_allow_html=True)
        
        # Gambar
        st.image(res_plotted, use_container_width=True)
        
        # Data
        boxes = results[0].boxes
        if len(boxes) > 0:
            st.success(f"Ditemukan {len(boxes)} objek sawit.")
        else:
            st.warning("Objek tidak terdeteksi dengan jelas.")
            
        st.markdown('</div>', unsafe_allow_html=True)
