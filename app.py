    import numpy as np
    import plotly.graph_objects as go

    if st.button("Generar espectro calibrado"):
        if len(pixeles) >= 2 and len(pixeles) == len(longitudes):
            # Asegurar orden creciente de píxeles
            pixeles_np = np.array(pixeles)
            longitudes_np = np.array(longitudes)

            # Ordenar por pixel
            sorted_indices = np.argsort(pixeles_np)
            pix_sorted = pixeles_np[sorted_indices]
            lambda_sorted = longitudes_np[sorted_indices]

            # Interpolación
            calibrated_axis = np.interp(x_axis, pix_sorted, lambda_sorted)

            # Gráfica calibrada
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

            # Mostrar tabla si se desea
            if st.checkbox("Mostrar datos calibrados (tabla)"):
                import pandas as pd
                df = pd.DataFrame({
                    "Longitud de onda (nm)": calibrated_axis,
                    "Intensidad": intensity
                })
                st.dataframe(df)
                st.download_button("Descargar como CSV", df.to_csv(index=False), "espectro_calibrado.csv", "text/csv")
        else:
            st.error("Debes ingresar al menos dos pares válidos de (píxel, longitud de onda).")
