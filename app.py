
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Cargar fuente
fuente = ImageFont.truetype("arial.ttf", 36)

st.title("🕒 Editor de Hora para Fotos de Reloj")
st.write("Subí una imagen de un reloj electrónico y reemplazá la hora con la que vos quieras.")

imagen_subida = st.file_uploader("📤 Subí una imagen", type=["jpg", "jpeg", "png"])
nueva_hora = st.text_input("🕓 Nueva fecha y hora (ej: 24-05-25 12:25:54)", "")

if imagen_subida and nueva_hora:
    imagen = Image.open(imagen_subida).convert("RGBA")

    # Crear capa de texto
    txt_layer = Image.new("RGBA", imagen.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # Medir texto
    text_bbox = draw.textbbox((0, 0), nueva_hora, font=fuente)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Posicionar en el centro
    x = (imagen.width - text_width) // 2
    y = (imagen.height - text_height) // 2

    # Dibujar fondo negro semitransparente
    padding = 10
    draw.rectangle(
        [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
        fill=(0, 0, 0, 180)
    )

    # Dibujar texto blanco
    draw.text((x, y), nueva_hora, font=fuente, fill=(255, 255, 255, 255))

    # Combinar capas
    imagen_final = Image.alpha_composite(imagen, txt_layer)

    st.image(imagen_final, caption="🖼️ Imagen modificada", use_column_width=True)

    # Descargar
    buffer = io.BytesIO()
    imagen_final.convert("RGB").save(buffer, format="JPEG")
    st.download_button("📥 Descargar imagen", buffer.getvalue(), file_name="imagen_editada.jpg")
