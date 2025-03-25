import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Espectroscopía DIY", layout="wide")
st.title("🔬 Espectroscopía DIY - Paso 1 y 2")

# Paso 1: Captura de la imagen
st.header("Paso 1: Carga o captura de imagen del espectro")
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

# Paso 2: Selección de puntos de calibración
if image is not None:
    st.header("Paso 2: Selección de puntos de referencia")

    # Convertir la imagen a numpy
    image_np = np.array(image)

    st.write("Haz clic en al menos 2 puntos de referencia sobre el espectro para calibrarlo.")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=5,
        stroke_color="red",
        background_image=image_np,
        update_streamlit=True,
        height=image_np.shape[0],
        width=image_np.shape[1],
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        coords = [(int(obj["left"]), int(obj["top"])) for obj in objects]

        if coords:
            st.success(f"{len(coords)} punto(s) seleccionado(s).")
            st.write("Coordenadas seleccionadas (x, y):")
            st.table(coords)
        else:
            st.warning("Selecciona al menos 2 puntos para calibrar el espectro.")
else:
    st.info("Por favor, sube una imagen o toma una foto para continuar.")
