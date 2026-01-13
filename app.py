import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

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
    # Pastikan file best.pt ada di folder yang sama
    return YOLO("best.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error memuat model: {e}. Pastikan file 'best.pt' tersedia.")
    st.stop()

# ---------------------------------------------------------------------
# 3. CSS: TEMA MODERN & ACADEMIC (CLEAN)
# ---------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap');

    /* BACKGROUND UTAMA - Grid Halus & Gelap */
    .stApp {
        background-color: #0f172a;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #e2e8f0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* JUDUL HALAMAN */
    h1 {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #f8fafc;
        margin-bottom: 10px;
        border-bottom: 2px solid #334155;
        padding-bottom: 20px;
    }
    
    /* CUSTOM TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 5px 5px 0 0;
        color: #94a3b8;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b;
        color: #4ade80;
        border-bottom: 2px solid #4ade80;
    }

    /* STYLE UNTUK INFORMASI (TABEL RAPI) */
    .info-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        backdrop-filter: blur(5px);
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #334155;
    }

    .info-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: #94a3b8; /* Slate 400 */
        font-weight: 600;
    }

    .info-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.2rem;
        color: #f1f5f9;
        font-weight: normal;
    }

    /* HILANGKAN ELEMENT BAWAAN STREAMLIT YANG MENGGANGGU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. UI UTAMA & LOGIKA
# ---------------------------------------------------------------------

st.title("SISTEM DETEKSI KEMATANGAN SAWIT")
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -10px; margin-bottom: 30px;'>Analisis Citra Digital Berbasis Deep Learning</p>", unsafe_allow_html=True)

# Membuat Tab agar UI tetap bersih (Upload vs Kamera)
tab1, tab2 = st.tabs(["📁 UPLOAD FILE", "📷 KAMERA LIVE"])

input_image = None
source_type = None

# --- TAB 1: UPLOAD FILE ---
with tab1:
    uploaded_file = st.file_uploader("Pilih file gambar (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
    if uploaded_file:
        input_image = Image.open(uploaded_file)
        source_type = "Upload File"

# --- TAB 2: KAMERA ---
with tab2:
    camera_file = st.camera_input("Ambil gambar langsung")
    if camera_file:
        input_image = Image.open(camera_file)
        source_type = "Kamera Langsung"

# ---------------------------------------------------------------------
# 5. PROSES DETEKSI & TAMPILAN HASIL
# ---------------------------------------------------------------------
if input_image is not None:
    st.write("---") # Garis pemisah
    
    # Tampilkan spinner saat proses
    with st.spinner(f'Sedang Menganalisis Citra dari {source_type}...'):
        
        # Lakukan Inferensi (Deteksi)
        results = model(input_image)
        
        # Ambil hasil bounding box untuk data tabel
        boxes = results[0].boxes 
        
        # Render ulang gambar dengan kotak deteksi (Plotting)
        # Plot mengembalikan array numpy BGR, perlu convert ke RGB
        res_plotted = results[0].plot()[:, :, ::-1] 

        # Tampilkan Gambar Hasil
        st.image(res_plotted, caption=f"Hasil Analisis ({source_type})", use_column_width=True)

        # ---------------------------------------------------------------------
        # 6. TABEL INFORMASI (Sesuai Request User)
        # ---------------------------------------------------------------------
        st.markdown(f"""
        <div class="info-container">
            <div class="info-row">
                <span class="info-label">Jumlah Terdeteksi</span>
                <span class="info-value">{len(boxes)} Buah</span>
            </div>
            <div class="info-row">
                <span class="info-label">Status Deteksi</span>
                <span class="info-value" style="color: {'#4ade80' if len(boxes) > 0 else '#f87171'}; text-shadow: 0 0 10px {'rgba(74, 222, 128, 0.3)' if len(boxes) > 0 else 'rgba(248, 113, 113, 0.3)'};">
                    {'BERHASIL' if len(boxes) > 0 else 'TIDAK ADA OBJEK'}
                </span>
            </div>
            <div class="info-row" style="border-bottom: none;">
                <span class="info-label">Model AI</span>
                <span class="info-value">YOLOv11 Nano</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Pesan default jika belum ada input
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #64748b; font-size: 0.9rem;">
        Pilih salah satu metode di atas (Upload atau Kamera) untuk memulai.
    </div>
    """, unsafe_allow_html=True)
