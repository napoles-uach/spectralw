# streamlit_app.py

import streamlit as st
from PIL import Image
import numpy as np

st.title("Espectroscopía DIY - Paso 1: Subir imagen espectral")

# Subir la imagen
uploaded_file = st.file_uploader("Sube una imagen del espectro (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Cargar y mostrar la imagen
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen del espectro", use_column_width=True)

    # Convertir a numpy para pasos posteriores
    image_np = np.array(image)

    st.write(f"Dimensiones de la imagen: {image_np.shape}")
else:
    st.info("Por favor, sube una imagen para comenzar.")
