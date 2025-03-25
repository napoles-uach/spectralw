import streamlit as st
from PIL import Image
import numpy as np
import plotly.graph_objects as go

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

    # Convertir a escala de grises si es RGB
    if len(image_np.shape) == 3:
        gray_image = np.mean(image_np, axis=2)
    else:
        gray_image = image_np

    # Selección de orientación
    orientation = st.selectbox("Orientación del espectro", ["Horizontal (colores a lo largo del eje x)", "Vertical (colores a lo largo del eje y)"])

    # Cálculo del perfil
    if "Horizontal" in orientation:
        intensity = np.mean(gray_image, axis=0)
        x_axis = np.arange(len(intensity))
    else:
        intensity = np.mean(gray_image, axis=1)
        x_axis = np.arange(len(intensity))

    # Crear gráfica interactiva con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=intensity, mode='lines', line=dict(color='black')))
    fig.update_layout(
        title="Espectro (sin calibrar)",
        xaxis_title="Posición en píxeles",
        yaxis_title="Intensidad promedio",
        height=400,
        margin=dict(l=40, r=20, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Primero debes subir o capturar una imagen.")

st.subheader("Paso opcional: Ingresar picos conocidos para calibración")

    # Recolectar entradas manuales
num_picos = st.number_input("¿Cuántos picos quieres ingresar?", min_value=1, max_value=10, value=2, step=1)

pixeles = []
longitudes = []

col1, col2 = st.columns(2)
with col1:
        st.markdown("**Posiciones en píxeles (observadas en la gráfica)**")
        for i in range(num_picos):
            p = st.number_input(f"Pico #{i+1} - posición (px)", key=f"px_{i}")
            pixeles.append(p)

with col2:
        st.markdown("**Longitudes de onda reales (en nm, por ejemplo)**")
        for i in range(num_picos):
            l = st.number_input(f"Pico #{i+1} - λ real", key=f"lambda_{i}")
            longitudes.append(l)

if st.button("Mostrar datos de calibración"):
        st.write("Picos seleccionados:")
        for i in range(num_picos):
            st.write(f"Pixel: {pixeles[i]} → Longitud de onda: {longitudes[i]} nm")
