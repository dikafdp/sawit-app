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

    /* BUTTON UPLOAD */
    .stFileUploader label {
        font-size: 1rem;
        color: #cbd5e1;
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
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: -10px;'>Analisis Citra Digital Berbasis Deep Learning</p>", unsafe_allow_html=True)

# Upload Section
uploaded_file = st.file_uploader("Unggah Citra Sawit (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Tampilkan spinner saat proses
    with st.spinner('Sedang Menganalisis Citra...'):
        # Buka gambar
        image = Image.open(uploaded_file)
        
        # Lakukan Inferensi (Deteksi)
        results = model(image)
        
        # Ambil hasil bounding box untuk data tabel
        # results[0].boxes adalah container untuk hasil deteksi
        boxes = results[0].boxes 
        
        # Render ulang gambar dengan kotak deteksi (Plotting)
        res_plotted = results[0].plot()[:, :, ::-1] # Konversi BGR ke RGB untuk PIL

        # Tampilkan Gambar Hasil
        st.image(res_plotted, caption="Hasil Visualisasi Deteksi", use_column_width=True)

        # ---------------------------------------------------------------------
        # 5. INTEGRASI TABEL INFORMASI (Sesuai Request)
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
    # Tampilan awal jika belum upload
    st.markdown("""
    <div style="text-align: center; padding: 50px; border: 2px dashed #334155; border-radius: 10px; color: #64748b;">
        Silakan unggah gambar buah sawit untuk memulai analisis.
    </div>
    """, unsafe_allow_html=True)
