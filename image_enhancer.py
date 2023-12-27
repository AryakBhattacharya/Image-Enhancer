import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Custom styling for the header
header_style = """
    color: #f63366;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1.5rem;
"""

# Add a styled header using markdown
st.markdown("<p style='{}'>Upload Image to Enhance</p>".format(header_style), unsafe_allow_html=True)


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
