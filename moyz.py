import streamlit as st
from PIL import Image
import io

st.title("Image Compressor with Streamlit")

uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    quality = st.slider("Compression Quality", min_value=10, max_value=95, value=50)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    st.download_button(
        label="Download Compressed Image",
        data=buffer,
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )
