import streamlit as st
from PIL import Image, ImageEnhance
import io

def adjust_image(image, brightness, contrast, saturation, sharpness):
    # Adjust Brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    # Adjust Contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    # Adjust Saturation
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation)

    # Adjust Sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)

    return image

# Page Title
st.title("Photo Editor")

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Open image using PIL
    image = Image.open(uploaded_image)

    # Display original image
    st.image(image, caption="Original Image", use_container_width=True)

    # Sliders for adjusting image properties
    brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
    contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
    saturation = st.slider("Saturation", 0.0, 2.0, 1.0)
    sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0)

    # Adjust the image based on slider values
    adjusted_image = adjust_image(image, brightness, contrast, saturation, sharpness)

    # Display adjusted image
    st.image(adjusted_image, caption="Adjusted Image", use_container_width=True)

    # Save the adjusted image for download
    if st.button("Download Adjusted Image"):
        # Save the image to a BytesIO object
        img_byte_arr = io.BytesIO()
        adjusted_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Provide the download link
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="adjusted_image.png",
            mime="image/png"
        )
