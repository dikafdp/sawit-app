import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time
import cv2
import av
from streamlit_webrtc import webrtc_streamer

st.set_page_config(
    page_title="Sistem Deteksi Sawit",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# LOAD MODEL
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# THEME

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Share+Tech+Mono&display=swap');

    /* BACKGROUND */
    .stApp {
        background-color: #020617;
        background-image: 
            radial-gradient(circle at 50% 0%, #1e293b 0%, transparent 70%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        font-family: 'Rajdhani', sans-serif;
    }

    /* COLORS */
    h1, h2, h3, p, span, div, label, small { color: #e2e8f0; }

    /* TITLE */
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

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid rgba(56, 189, 248, 0.2); }
    .stTabs [data-baseweb="tab"] { background-color: rgba(15, 23, 42, 0.5); border-radius: 4px 4px 0 0; color: #94a3b8; font-family: 'Share Tech Mono', monospace; border: 1px solid transparent; }
    .stTabs [aria-selected="true"] { background-color: rgba(56, 189, 248, 0.1) !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important; border-bottom: none !important; }
    div[data-baseweb="tab-highlight"] { background-color: #38bdf8 !important; }

    /* COMPONENTS */
    [data-testid="stCameraInput"], [data-testid="stFileUploader"], .rtc-container {
        border: 1px solid rgba(56, 189, 248, 0.3); background: rgba(15, 23, 42, 0.8); border-radius: 6px; padding: 10px;
    }
    
    .streamlit-expanderHeader {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }

    /* BUTTONS */
    button {
        background-color: transparent !important; border: 1px solid #38bdf8 !important; color: #38bdf8 !important;
        font-family: 'Share Tech Mono', monospace !important; text-transform: uppercase; letter-spacing: 2px;
        transition: all 0.3s ease; border-radius: 4px !important;
    }
    button:hover { background-color: rgba(56, 189, 248, 0.1) !important; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }

    .tech-card {
        background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-left: 3px solid #38bdf8;
        backdrop-filter: blur(10px); padding: 25px; margin-top: 30px; position: relative;
    }
    .tech-card::before { content: ""; position: absolute; top: -1px; right: -1px; width: 15px; height: 15px; border-top: 1px solid #38bdf8; border-right: 1px solid #38bdf8; }
    
    .data-header {
        font-family: 'Share Tech Mono', monospace; color: #94a3b8; font-size: 0.85rem; letter-spacing: 1px;
        display: block; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;
    }

    .info-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid rgba(56, 189, 248, 0.2); }
    .data-label { font-family: 'Share Tech Mono', monospace; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; }
    .data-value { font-family: 'Rajdhani', sans-serif; font-size: 1.3rem; font-weight: 700; color: #f1f5f9; text-align: right; }

    .status-bar {
        display: flex; justify-content: space-between; background: rgba(0,0,0,0.2); border-top: 1px solid rgba(255,255,255,0.1);
        padding: 10px 15px; margin-top: 25px; border-radius: 4px; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: #38bdf8;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# SESSION STATE
if 'conf' not in st.session_state: st.session_state.conf = 0.25
if 'iou' not in st.session_state: st.session_state.iou = 0.45
if 'line_width' not in st.session_state: st.session_state.line_width = 2

# Callback Real-time
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    results = model(img, conf=st.session_state.conf, iou=st.session_state.iou)
    res_plotted = results[0].plot(line_width=st.session_state.line_width)
    return av.VideoFrame.from_ndarray(res_plotted, format="bgr24")


st.markdown("<h1>SISTEM DETEKSI KEMATANGAN SAWIT</h1>", unsafe_allow_html=True)
st.markdown('<div class="tech-subtitle">/// IMPLEMENTASI ALGORITMA DEEP LEARNING YOLOV11 ///</div>', unsafe_allow_html=True)

# PANEL KONTROL
with st.expander("⚙️ PANEL KONTROL PARAMETER"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.conf = st.slider("Confidence", 0.0, 1.0, 0.25, 0.05)
    with c2:
        st.session_state.iou = st.slider("IoU Threshold", 0.0, 1.0, 0.45, 0.05)
    with c3:
        st.session_state.line_width = st.slider("Tebal Garis", 1, 5, 2, 1)

tab1, tab2, tab3 = st.tabs(["📸 SNAPSHOT", "📂 UPLOAD", "🔴 REAL-TIME"])

img_file = None
is_static = False

with tab1:
    cam = st.camera_input("Kamera", label_visibility="hidden")
    if cam: 
        img_file = cam
        is_static = True

with tab2:
    upl = st.file_uploader("Upload", type=['jpg','png','jpeg'], label_visibility="hidden")
    if upl: 
        img_file = upl
        is_static = True

with tab3:
    st.markdown('<div class="rtc-container">', unsafe_allow_html=True)
    webrtc_streamer(
        key="sawit-realtime",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# LOGIC
if is_static and img_file is not None:
    image = Image.open(img_file)
    
    # Progress Bar
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        bar.progress(i+1)
        
    # Deteksi
    results = model(image, conf=st.session_state.conf, iou=st.session_state.iou)
    res_plotted = results[0].plot(line_width=st.session_state.line_width)[:, :, ::-1]
    boxes = results[0].boxes
    
    # Perhitungan Data
    jml_objek = len(boxes)
    if jml_objek > 0:
        avg_conf = boxes.conf.mean().item() * 100
        akurasi_text = f"{avg_conf:.1f}%"
        status_text = "BERHASIL"
        status_color = "#4ade80"
    else:
        akurasi_text = "0%"
        status_text = "TIDAK JELAS"
        status_color = "#f472b6"

    st.markdown('<div class="tech-card">', unsafe_allow_html=True)
    st.markdown('<span class="data-header">>> HASIL KLASIFIKASI CITRA</span>', unsafe_allow_html=True)
    
    st.image(res_plotted, use_container_width=True)
    
    html_tabel = f"""
<div style="margin-top: 20px;">
    <div class="info-row">
        <span class="data-label">JUMLAH OBJEK</span>
        <span class="data-value">{jml_objek} UNIT</span>
    </div>
    <div class="info-row">
        <span class="data-label">RATA-RATA AKURASI</span>
        <span class="data-value" style="color: #38bdf8;">{akurasi_text}</span>
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
"""
    
    # Render HTML
    st.markdown(html_tabel, unsafe_allow_html=True)

    # Footer
    st.markdown(f'''
        <div class="status-bar">
            <span>CONF: {st.session_state.conf}</span>
            <span>IOU: {st.session_state.iou}</span>
            <span>MODUL: CV-PYTORCH</span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

