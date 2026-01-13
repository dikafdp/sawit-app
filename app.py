import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Deteksi Sawit Cloud", page_icon="🌴")
st.title("🌴 Deteksi Sawit (Mode Foto)")
st.write("Arahkan kamera ke buah sawit, lalu klik tombol **Take Photo**.")

# Load Model (Cache supaya cepat)
@st.cache_resource
def load_model():
    return YOLO("best.pt")

try:
    model = load_model()
except Exception as e:
    st.error("Model best.pt tidak ditemukan. Pastikan file ada di GitHub.")

# --- FITUR UTAMA: KAMERA JEPRET ---
img_file = st.camera_input("Kamera")

if img_file is not None:
    # 1. Buka gambar
    image = Image.open(img_file)
    
    # 2. Deteksi dengan YOLO
    with st.spinner('Sedang menganalisa...'):
        results = model(image)
        
        # 3. Tampilkan Hasil (Plotting)
        # YOLO menyimpan warna BGR, kita balik ke RGB biar warnanya benar
        res_plotted = results[0].plot()[:, :, ::-1]
        
        st.image(res_plotted, caption="Hasil Deteksi AI", use_container_width=True)
        
        # 4. Teks Label (Opsional)
        # Menampilkan jumlah buah yang terdeteksi
        boxes = results[0].boxes
        if len(boxes) > 0:
            st.success(f"Ditemukan {len(boxes)} objek sawit.")
        else:
            st.warning("Tidak ada sawit terdeteksi.")

# Masukkan ini di app.py Anda
def load_css_file(css_file_path):
    # Cek apakah file benar-benar ada di sebelah app.py
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Jika file tidak ketemu (mungkin lupa upload), pakai style darurat
        st.warning(f"File {css_file_path} tidak ditemukan di GitHub!")
