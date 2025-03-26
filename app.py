import streamlit as st
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.title("Espectroscopía DIY - Generación del espectro (con calibración y recorte)")

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

# Paso 2: Procesar imagen si fue cargada
if image is not None:
    st.image(image, caption="Imagen original", use_column_width=True)

    width, height = image.size
    st.subheader("Recorte de la región de interés (opcional)")
    st.markdown("Define las coordenadas para recortar la imagen (en píxeles):")

    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("x0 (inicio horizontal)", min_value=0, max_value=width-1, value=0)
        x1 = st.number_input("x1 (fin horizontal)", min_value=1, max_value=width, value=width)
    with col2:
        y0 = st.number_input("y0 (inicio vertical)", min_value=0, max_value=height-1, value=0)
        y1 = st.number_input("y1 (fin vertical)", min_value=1, max_value=height, value=height)

    # Recortar imagen
    cropped_image = image.crop((x0, y0, x1, y1))
    st.image(cropped_image, caption="Imagen recortada", use_column_width=True)

    # Convertir a numpy
    image_np = np.array(cropped_image)
    st.write(f"Dimensiones de la imagen recortada: {image_np.shape}")

    # Convertir a escala de grises
    if len(image_np.shape) == 3:
        gray_image = np.mean(image_np, axis=2)
    else:
        gray_image = image_np

    # Orientación del espectro
    orientation = st.selectbox("Orientación del espectro", ["Horizontal (colores a lo largo del eje x)", "Vertical (colores a lo largo del eje y)"])

    # Perfil de intensidad
    if "Horizontal" in orientation:
        intensity = np.mean(gray_image, axis=0)
        x_axis = np.arange(len(intensity))
    else:
        intensity = np.mean(gray_image, axis=1)
        x_axis = np.arange(len(intensity))

    # Espectro sin calibrar
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

    # Entrada de picos conocidos
    st.subheader("Paso opcional: Ingresar picos conocidos para calibración")
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
        st.markdown("**Longitudes de onda reales (en nm)**")
        for i in range(num_picos):
            l = st.number_input(f"Pico #{i+1} - λ real", key=f"lambda_{i}")
            longitudes.append(l)

    # Interpolación con extrapolación
    def interpolate_with_extrapolation(x, xp, fp):
        interp = np.interp(x, xp, fp)
        left_mask = x < xp[0]
        interp[left_mask] = fp[0] + (x[left_mask] - xp[0]) * (fp[1] - fp[0]) / (xp[1] - xp[0])
        right_mask = x > xp[-1]
        interp[right_mask] = fp[-1] + (x[right_mask] - xp[-1]) * (fp[-1] - fp[-2]) / (xp[-1] - xp[-2])
        return interp

    if st.button("Generar espectro calibrado"):
        if len(pixeles) >= 2 and len(pixeles) == len(longitudes):
            pixeles_np = np.array(pixeles)
            longitudes_np = np.array(longitudes)

            sorted_indices = np.argsort(pixeles_np)
            pix_sorted = pixeles_np[sorted_indices]
            lambda_sorted = longitudes_np[sorted_indices]

            calibrated_axis = interpolate_with_extrapolation(x_axis, pix_sorted, lambda_sorted)

            # Espectro calibrado
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=calibrated_axis, y=intensity, mode='lines', line=dict(color='blue')))
            fig2.update_layout(
                title="Espectro calibrado",
                xaxis_title="Longitud de onda (nm)",
                yaxis_title="Intensidad promedio",
                height=400,
                margin=dict(l=40, r=20, t=40, b=40)
            )
            st.plotly_chart(fig2, use_container_width=True)

            if st.checkbox("Mostrar datos calibrados (tabla)"):
                df = pd.DataFrame({
                    "Longitud de onda (nm)": calibrated_axis,
                    "Intensidad": intensity
                })
                st.dataframe(df)
                st.download_button("Descargar como CSV", df.to_csv(index=False), "espectro_calibrado.csv", "text/csv")
        else:
            st.error("Debes ingresar al menos dos pares válidos de (píxel, longitud de onda).")
else:
    st.info("Primero debes subir o capturar una imagen.")

