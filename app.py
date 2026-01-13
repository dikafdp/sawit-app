import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
from ultralytics import YOLO

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Live Deteksi Sawit", page_icon="🌴")
st.title("🌴 Real-Time Sawit Detection")

# 2. Load Model (Cache biar kencang)
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# 3. Fungsi Callback (Ini Jantungnya)
# Fungsi ini dipanggil puluhan kali per detik untuk setiap frame video
def video_frame_callback(frame):
    # a. Ambil gambar dari kamera (format AV -> NumPy)
    img = frame.to_ndarray(format="bgr24")

    # b. Deteksi dengan YOLO
    # conf=0.5 artinya hanya tampilkan yang yakin > 50%
    results = model(img, conf=0.5)

    # c. Gambar kotak hasil ke gambar
    annotated_frame = results[0].plot()

    # d. Kembalikan gambar yang sudah dicoret-coret ke layar (NumPy -> AV)
    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")

# 4. Tampilkan WebRTC Streamer
st.write("Tekan **START** untuk memulai kamera.")

webrtc_streamer(
    key="sawit-live", 
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False}, # Hanya video, tanpa suara
    rtc_configuration={  # Konfigurasi server STUN (biar lancar di HP)
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)