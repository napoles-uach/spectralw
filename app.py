import streamlit as st
from PIL import Image
import numpy as np

st.title("Espectroscopía DIY - Paso 1: Captura del espectro")

# Selector de método
method = st.radio("¿Cómo deseas cargar la imagen?", ["Subir desde archivo", "Usar cámara"])

image = None

if method == "Subir desde archivo":
    uploaded_file = st.file_uploader("Sube una imagen del espectro", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

elif method == "Usar cámara":
    camera_image = st.camera_input("Toma una foto del espectro")
    if camera_image is not None:
        image = Image.open(camera_image)

# Mostrar imagen cargada
if image is not None:
    st.image(image, caption="Imagen del espectro", use_column_width=True)

    # Convertir a numpy array
    image_np = np.array(image)
    st.write(f"Dimensiones de la imagen: {image_np.shape}")
else:
    st.info("Por favor, proporciona una imagen para continuar.")
