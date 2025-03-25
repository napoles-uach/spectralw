import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

st.title("Espectroscopía DIY - Generación del espectro (sin calibrar)")

# Paso 1: Cargar imagen
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

# Paso 2: Mostrar y procesar la imagen
if image is not None:
    st.image(image, caption="Imagen del espectro", use_column_width=True)

    image_np = np.array(image)
    
    st.write(f"Dimensiones de la imagen: {image_np.shape}")

    # Convertir a escala de grises si es necesario
    if len(image_np.shape) == 3:
        gray_image = np.mean(image_np, axis=2)  # promedio de R, G, B
    else:
        gray_image = image_np  # ya es gris

    # Detectar si el espectro es horizontal o vertical
    orientation = st.selectbox("Orientación del espectro", ["Horizontal (colores a lo largo del eje x)", "Vertical (colores a lo largo del eje y)"])

    # Generar perfil de intensidad
    if "Horizontal" in orientation:
        intensity = np.mean(gray_image, axis=0)  # promedio por columna
        x_axis = np.arange(len(intensity))
    else:
        intensity = np.mean(gray_image, axis=1)  # promedio por fila
        x_axis = np.arange(len(intensity))

    # Graficar el espectro
    fig, ax = plt.subplots()
    ax.plot(x_axis, intensity, color='black')
    ax.set_title("Espectro (sin calibrar)")
    ax.set_xlabel("Posición en píxeles")
    ax.set_ylabel("Intensidad promedio")
    st.pyplot(fig)
