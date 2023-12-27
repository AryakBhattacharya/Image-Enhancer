import cv2
import os
import streamlit as st
import numpy as np
from PIL import Image, ImageFilter
from io import BytesIO

# Set the root path for saving images
root_path = '/content/drive/MyDrive/Colab Notebooks/Image Enhancing'

# Create a new folder for saving images if it doesn't exist
output_folder = 'Enhanced_Images'
output_path = f'{root_path}/{output_folder}'

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

# Create the output directory if it doesn't exist
create_directory(root_path)
create_directory(output_path)

# Function to upload an image file
def upload_image():
    uploaded = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        return uploaded
    return None

# Function to enhance image quality without resizing
def enhance_image(input_image_path):
    # Read the image
    img = cv2.imread(input_image_path)

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

# Function to save images
def save_images(original_image, enhanced_image, output_path, image_name):
    original_path = f'{output_path}/{image_name}_original.png'
    enhanced_path = f'{output_path}/{image_name}_enhanced.png'

    cv2.imwrite(original_path, original_image)
    cv2.imwrite(enhanced_path, enhanced_image)

    st.success(f"Original image saved to: {original_path}")
    st.success(f"Enhanced image saved to: {enhanced_path}")

# Main program
# Upload image
image = upload_image()

if image is not None:
    # Read the image
    image_path = f'{output_path}/uploaded_image.png'

    # Create the directory if it doesn't exist
    create_directory(os.path.dirname(image_path))

    img = Image.open(image)
    img.save(image_path)

    # Enhance the image without resizing
    enhanced_image = enhance_image(image_path)

    # Display the original and enhanced images
    st.image(img, caption="Original Image", use_column_width=True)
    display_image(enhanced_image)

    # Save images to Google Drive
    image_name = 'uploaded_image'
    save_images(cv2.imread(image_path), enhanced_image, output_path, image_name)
