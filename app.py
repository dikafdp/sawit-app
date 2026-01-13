import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

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
    return YOLO("best.pt")

model = load_model() # Load di awal agar global

# ---------------------------------------------------------------------
# 3. CSS: TEMA ACADEMIC TECH (SESUAI GAMBAR)
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

    h1, h2, h3, p, span, div, label, small { color: #e2e8f0; }

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
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .tech-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #38bdf8;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* CUSTOM TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.5);
        border-radius: 4px 4px 0 0;
        color: #94a3b8;
        font-family: 'Share Tech Mono', monospace;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.1) !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-bottom: none !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #38bdf8 !important;
    }

    /* INPUTS & BUTTONS */
    [data-testid="stCameraInput"], [data-testid="stFileUploader"], .rtc-container {
        border: 1px solid rgba(56, 189, 248, 0.3);
        background: rgba(15, 23, 42, 0.8);
        border-radius: 6px;
        padding: 10px;
    }
    
    /* Tombol Umum & WebRTC Button */
    button {
        background-color: transparent !important;
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
        font-family: 'Share Tech Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        border-radius: 4px !important;
    }
    button:hover {
        background-color: rgba(56, 189, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }

    /* KARTU HASIL */
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

    .data-label {
        font-family: 'Share Tech Mono', monospace;
        color: #94a3b8; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase;
    }
    .data-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem; font-weight: 700; color: #f1f5f9; text-align: right;
    }

    .info-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 0; border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    }

    .status-bar {
        display: flex; justify-content: space-between;
        background: rgba(0,0,0,0.2);
        border-top: 1px solid rgba(255,255,255,0.1);
        padding: 10px 15px; margin-top: 25px; border-radius: 4px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem; color: #38bdf8;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 4. LOGIKA REAL-TIME PROCESSING
# ---------------------------------------------------------------------
class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Deteksi Langsung
        results = model(img)
        
        # Gambar Kotak Deteksi di Video
        res_plotted = results[0].plot()
        
        return av.VideoFrame.from_ndarray(res_plotted, format="bgr24")

# ---------------------------------------------------------------------
# 5. UI UTAMA
# ---------------------------------------------------------------------

st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<div class="tech-subtitle">/// IMPLEMENTASI ALGORITMA DEEP LEARNING YOLOV11 ///</div>', unsafe_allow_html=True)

# TAB BARU: REAL-TIME
tab1, tab2, tab3 = st.tabs(["📸 FOTO SNAPSHOT", "📂 UPLOAD FILE", "🔴 REAL-TIME"])

img_file = None
run_detection = False # Flag untuk tab 1 & 2

# --- TAB 1: SNAPSHOT ---
with tab1:
    st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ AMBIL FOTO ]</p>', unsafe_allow_html=True)
    cam = st.camera_input("Kamera", label_visibility="hidden")
    if cam: 
        img_file = cam
        run_detection = True

# --- TAB 2: UPLOAD ---
with tab2:
    st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ PILIH DARI GALERI ]</p>', unsafe_allow_html=True)
    upl = st.file_uploader("Upload", type=['jpg','png','jpeg'], label_visibility="hidden")
    if upl: 
        img_file = upl
        run_detection = True

# --- TAB 3: REAL-TIME VIDEO ---
with tab3:
    st.markdown('<p style="text-align:center; font-family:Share Tech Mono; font-size:0.9rem; color:#94a3b8;">[ STREAMING DETEKSI LANGSUNG ]</p>', unsafe_allow_html=True)
    
    # Bungkus WebRTC dalam container agar CSS tombolnya kena style
    st.markdown('<div class="rtc-container">', unsafe_allow_html=True)
    
    webrtc_streamer(
        key="sawit-realtime",
        video_processor_factory=VideoProcessor,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("ℹ️ Klik 'START' untuk memulai kamera. Pastikan memberikan izin akses browser.")


# --- PROSES UNTUK TAB 1 & 2 (FOTO) ---
if run_detection and img_file is not None:
    image = Image.open(img_file)
    
    # Animasi Loading
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)
    
    # Deteksi
    results = model(image)
    res_plotted = results[0].plot()[:, :, ::-1]
    boxes = results[0].boxes
    
    # TAMPILAN HASIL (GAYA LIST VERTIKAL)
    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<span class="data-label" style="border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px; display:block;">>> HASIL KLASIFIKASI CITRA</span>', unsafe_allow_html=True)
    
    # Gambar
    st.image(res_plotted, use_container_width=True)
    
    # List Info
    status_text = "BERHASIL" if len(boxes) > 0 else "TIDAK JELAS"
    status_color = "#4ade80" if len(boxes) > 0 else "#f472b6"
    
    st.markdown(f"""
        <div style="margin-top: 20px;">
            <div class="info-row">
                <span class="data-label">JUMLAH OBJEK</span>
                <span class="data-value">{len(boxes)} UNIT</span>
            </div>
            <div class="info-row">
                <span class="data-label">STATUS DETEKSI</span>
                <span class="data-value" style="color: {status_color};">{status_text}</span>
            </div>
            <div class="info-row" style="border-bottom: none;">
                <span class="data-label">MODEL AI</span>
                <span class="data-value">YOLOv11 Nano</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown(f'''
        <div class="status-bar">
            <span>METODE: YOLOv11</span>
            <span>THRESHOLD: 0.25</span>
            <span>MODUL: CV-PYTORCH</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
