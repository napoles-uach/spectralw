import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

st.title("Espectroscopía DIY - Paso 2: Calibración del espectro")

# Paso 1: Subir o capturar imagen
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

# Paso 2: Selección de puntos
if image is not None:
    st.subheader("Haz clic en al menos 2 puntos de referencia sobre el espectro")
    image_np = np.array(image)

    # Canvas para dibujar sobre la imagen
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # rojo semitransparente
        stroke_width=5,
        stroke_color="red",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    # Mostrar coordenadas seleccionadas
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        coords = [(int(obj["left"]), int(obj["top"])) for obj in objects]
        st.write("Coordenadas seleccionadas (x, y):")
        st.write(coords)

        if len(coords) >= 2:
            st.success("¡Puntos suficientes para calibrar!")
        else:
            st.warning("Selecciona al menos dos puntos de referencia.")
else:
    st.info("Primero debes cargar una imagen.")
