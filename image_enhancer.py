import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

st.set_page_config(
    page_title="My Custom Streamlit App",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded",
)
css = """
body {
    color: #333;
    background-color: #fff;
}
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
with st.beta_container():
    st.write("Upload Image to Enhance")

# with st.beta_expander("Click me to expand"):
#     st.write("This is inside an expander!")
# st.set_theme("blue")


# Function to enhance image quality without resizing
def enhance_image(img):
    # Convert PIL image to OpenCV format
    img = np.array(img)

    # Increase deblurring effect (adjust the kernel size)
    img = cv2.GaussianBlur(img, (11, 11), 0)

    # Increase depixelation effect (adjust the interpolation method)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

    # Add sharpness and clarity
    img = cv2.filter2D(img, -1, kernel=np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))

    return img

# Function to save images
def save_images(original_image, enhanced_image):
    # Save the enhanced image to the Streamlit cache directory
    st.image(original_image, caption="Original Image", use_column_width=True)
    st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)

# Main program
# Upload image
image = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if image is not None:
    # Read the image
    img = Image.open(image)

    # Enhance the image without resizing
    enhanced_image = enhance_image(img)

    # Display the original and enhanced images
    save_images(img, enhanced_image)
