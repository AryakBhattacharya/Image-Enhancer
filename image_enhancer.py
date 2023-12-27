import cv2
import streamlit as st
import numpy as np
from PIL import Image
import os

# Install gdown
st.sidebar.text("Installing gdown...")
st.sidebar.text("This may take a minute.")
st.shell_command("pip install gdown")

import gdown

# Authenticate and mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Set the root path for saving images
root_path = '/content/drive/MyDrive/Colab Notebooks/Image Enhancing'

# Create a new folder for saving images if it doesn't exist
output_folder = 'Enhanced_Images'
output_path = f'{root_path}/{output_folder}'

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

# Function to upload an image file
def upload_image():
    uploaded = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        return uploaded
    return None

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

# Function to display the enhanced image
def display_image(image):
    st.image(image, caption="Enhanced Image", use_column_width=True)

# Function to save images to Google Drive
def save_images(original_image, enhanced_image, output_path, image_name):
    original_path = f'{output_path}/{image_name}_original.png'
    enhanced_path = f'{output_path}/{image_name}_enhanced.png'

    cv2.imwrite(original_path, original_image)
    cv2.imwrite(enhanced_path, enhanced_image)

    st.success(f"Original image saved to: {original_path}")
    st.success(f"Enhanced image saved to: {enhanced_path}")

# Main program
# Authenticate and mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Upload image
image = upload_image()

if image is not None:
    # Save the uploaded image to Google Drive
    image_name = 'uploaded_image'
    uploaded_image_path = f'{output_path}/{image_name}.png'
    with open(uploaded_image_path, 'wb') as f:
        f.write(image.read())

    # Enhance the image without resizing
    uploaded_image = Image.open(uploaded_image_path)
    enhanced_image = enhance_image(uploaded_image)

    # Display the original and enhanced images
    st.image(uploaded_image, caption="Original Image", use_column_width=True)
    display_image(enhanced_image)

    # Save images to Google Drive
    save_images(np.array(uploaded_image), enhanced_image, output_path, image_name)
