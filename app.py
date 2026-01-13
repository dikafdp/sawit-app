import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time

# ---------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Sistem Deteksi Sawit",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# 2. LOAD MODEL
# ---------------------------------------------------------------------
@st.cache_resource
def load_model():
    # Pastikan file best.pt ada di folder yang sama
    return YOLO("best.pt")

# ---------------------------------------------------------------------
# 3. CSS: TEMA "ACADEMIC TECH" (SESUAI GAMBAR)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT */
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

    /* TEXT COLOR */
    h1, h2, h3, p, span, div, label, small {
        color: #e2e8f0;
    }

    /* JUDUL UTAMA */
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
        margin-bottom: 5px;
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

    /* --- CUSTOM TABS (GARIS BIRU) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 4px 4px 0 0;
        color: #94a3b8;
        font-family: 'Share Tech Mono', monospace;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.1) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-bottom: none !important;
    }
    /* MENGUBAH GARIS INDIKATOR MERAH JADI BIRU */
    div[data-baseweb="tab-highlight"] {
        background-color: #38bdf8 !important;
    }

    /* --- TOMBOL --- */
    [data-testid="stCameraInput"], [data-testid="stFileUploader"] {
        border: 1px solid rgba(56, 189, 248, 0.3);
        background: rgba(15, 23, 42, 0.8);
        border-radius: 6px;
        padding: 10px;
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

    /* --- KARTU HASIL --- */
    .tech-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 3px solid #38bdf8;
        backdrop-filter: blur(10px);
        padding: 25px;
        margin-top: 30px;
        position: relative;
    }
    .tech-card::before {
        content: ""; position: absolute; top: -1px; right: -1px;
        width: 15px; height: 15px;
        border-top: 1px solid #38bdf8; border-right: 1px solid #38bdf8;
    }

    /* CSS KHUSUS UNTUK TAMPILAN LIST VERTIKAL (SEPERTI GAMBAR) */
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2); /* Garis tipis pemisah */
    }

    .data-label {
        font-family: 'Share Tech Mono', monospace;
        color: #94a3b8;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .data-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        text-align: right;
    }

    .tech-card img {
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-top: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    
    /* Footer Status */
    .status-bar {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 10px;
        margin-top: 25px;
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
    st.error("Error: File model 'best.pt' tidak ditemukan.")
    st.stop()

# --- HEADER ---
st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<div class="tech-subtitle">/// IMPLEMENTASI ALGORITMA DEEP LEARNING YOLOV11 ///</div>', unsafe_allow_html=True)

# --- PILIHAN INPUT (TABS) ---
tab1, tab2 = st.tabs(["📸 KAMERA LIVE", "📂 UPLOAD FILE"])
img_file = None

with tab1:
    st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ AMBIL FOTO LANGSUNG ]</p>', unsafe_allow_html=True)
    cam_input = st.camera_input("Kamera", label_visibility="hidden")
    if cam_input: img_file = cam_input

with tab2:
    st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ PILIH CITRA DARI GALERI ]</p>', unsafe_allow_html=True)
    upl_input = st.file_uploader("Upload", type=['jpg', 'png', 'jpeg'], label_visibility="hidden")
    if upl_input: img_file = upl_input

# --- PROSES & OUTPUT ---
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
    
    # --- TAMPILAN HASIL (SEPERTI GAMBAR: LIST VERTIKAL) ---
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    
    # Header Kartu
    st.markdown('<span class="data-label" style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:10px; display:block;">>> HASIL KLASIFIKASI CITRA</span>', unsafe_allow_html=True)
    
    # Gambar
    st.image(res_plotted, use_container_width=True)
    
    # INFORMASI DETEKSI (LIST VERTIKAL SESUAI GAMBAR)
    # Menggunakan HTML Flexbox agar rapi kiri-kanan
    
    # Baris 1: Jumlah
    st.markdown(f"""
        <div class="info-row">
            <span class="data-label">JUMLAH OBJEK</span>
            <span class="data-value">{len(boxes)} UNIT</span>
        </div>
    """, unsafe_allow_html=True)

    # Baris 2: Status (Warna Hijau/Merah)
    warna_status = "#4ade80" if len(boxes) > 0 else "#f472b6"
    text_status = "BERHASIL" if len(boxes) > 0 else "TIDAK JELAS"
    
    st.markdown(f"""
        <div class="info-row">
            <span class="data-label">STATUS DETEKSI</span>
            <span class="data-value" style="color: {warna_status};">{text_status}</span>
        </div>
    """, unsafe_allow_html=True)

    # Baris 3: Model (Tanpa Border Bawah)
    st.markdown(f"""
        <div class="info-row" style="border-bottom: none;">
            <span class="data-label">MODEL AI</span>
            <span class="data-value">YOLOv11 Nano</span>
        </div>
    """, unsafe_allow_html=True)

    # FOOTER TEKNIS
    st.markdown(f'''
        <div class="status-bar">
            <span>METODE: YOLOv11</span>
            <span>THRESHOLD: 0.25</span>
            <span>MODUL: CV-PYTORCH</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
