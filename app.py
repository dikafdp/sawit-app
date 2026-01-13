import streamlit as st
from ultralytics import YOLO
from PIL import Image

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN (WAJIB DI PALING ATAS)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Sawit AI - Premium Detection",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. CSS MODERN DARK MODE (GAYA SEPERTI GAMBAR REFERENSI)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* --- IMPORT FONT MODERN (INTER) --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* --- RESET DEFAULT STREAMLIT --- */
    .stApp {
        background-color: #0E0E10 !important; /* Latar belakang hitam pekat */
        font-family: 'Inter', sans-serif !important;
    }

    /* Warna teks default */
    h1, h2, h3, p, div, span, label {
        color: #FFFFFF !important;
    }

    /* --- JUDUL UTAMA --- */
    h1 {
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #ffffff, #a8a8a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    /* Subjudul */
    .sub-header {
        text-align: center;
        color: #8A8F98 !important; /* Abu-abu terang */
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* --- CUSTOMISASI TOMBOL KAMERA --- */
    /* Target elemen pembungkus kamera */
    [data-testid="stCameraInput"] {
        border: 1px solid #2D3339;
        background-color: #1C1C21;
        border-radius: 16px;
        padding: 10px;
    }

    /* Target tombol "Take Photo" di dalamnya */
    [data-testid="stCameraInput"] button {
        background-color: #FFFFFF !important;
        color: #0E0E10 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efek Hover Tombol */
    [data-testid="stCameraInput"] button:hover {
        background-color: #E1E1E1 !important;
        transform: scale(1.02);
    }

    /* --- KOTAK HASIL (PREMIUM DARK CARD) --- */
    .hasil-card {
        background-color: #1C1C21; /* Abu-abu sangat tua (seperti di referensi) */
        border: 1px solid #2D3339; /* Garis tepi halus */
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        margin-top: 40px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); /* Bayangan lembut */
        animation: fadeUp 0.6s ease-out;
    }

    /* Judul di dalam kartu hasil */
    .hasil-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #8A8F98 !important;
        margin-bottom: 20px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Gambar hasil */
    .hasil-card img {
        border-radius: 16px;
        border: 1px solid #2D3339;
    }
    
    /* Animasi Muncul */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* --- STATISTIK HASIL (Badge) --- */
    .stat-badge-success {
        display: inline-block;
        background: rgba(46, 204, 113, 0.15); /* Hijau transparan */
        color: #2ecc71 !important; /* Teks Hijau Neon */
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

    /* Hilangkan elemen footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 3. LOGIKA APLIKASI
# ---------------------------------------------------------------------

# Load Model (Cache)
@st.cache_resource
def load_model():
    # Pastikan file best.pt ada di folder yang sama
    return YOLO("best.pt")

try:
    model = load_model()
except Exception:
    st.error("⚠️ File model 'best.pt' tidak ditemukan.")
    st.stop()

# --- HEADER ---
st.title("Sawit AI")
st.markdown('<p class="sub-header">Advanced Computer Vision for Palm Oil Maturity Detection</p>', unsafe_allow_html=True)

# --- AREA KAMERA ---
# Kita buat kolom agar kamera tidak terlalu lebar
col_spacer1, col_cam, col_spacer2 = st.columns([1, 4, 1])

with col_cam:
    img_file = st.camera_input("Label Tersembunyi", label_visibility="hidden")

# --- PROSES & HASIL ---
if img_file is not None:
    image = Image.open(img_file)
    
    # Spinner modern (akan mengikuti tema gelap)
    with st.spinner('Processing Image...'):
        # Deteksi
        results = model(image)
        # Balik warna BGR ke RGB untuk ditampilkan
        res_plotted = results[0].plot()[:, :, ::-1]
        
        # --- TAMPILAN HASIL (KARTU PREMIUM) ---
        st.markdown('<div class="hasil-card">', unsafe_allow_html=True)
        st.markdown('<span class="hasil-label">Analysis Results</span>', unsafe_allow_html=True)
        
        # Gambar Hasil
        st.image(res_plotted, use_container_width=True)
        
        # Data Statistik
        boxes = results[0].boxes
        if len(boxes) > 0:
            # Tampilkan badge sukses
            st.markdown(f'<div class="stat-badge-success">✨ {len(boxes)} Objects Detected Successfully</div>', unsafe_allow_html=True)
        else:
            # Tampilkan badge peringatan
            st.markdown('<div class="stat-badge-warning">⚠️ No Objects Detected</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
