import streamlit as st
import numpy as np
from PIL import Image
import webcolors

# Function to find closest CSS3 color name
def closest_color(requested_color):
    min_colors = {}
    for hex_code, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

# Streamlit UI
st.title("Color Detection Application")

uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert to numpy array
    img_array = np.array(image.convert('RGB'))

    st.write("Click on the image to detect color:")

    # Get click coordinates using Streamlit's experimental features
    click = st.experimental_data_editor(pd.DataFrame(), num_rows=1, key="click_coords")
    
    # Alternative simpler approach: Use st.slider to input X and Y coordinates
    width, height = image.size
    x = st.slider("X coordinate", 0, width - 1, width // 2)
    y = st.slider("Y coordinate", 0, height - 1, height // 2)

    r, g, b = img_array[y, x]
    color_name = closest_color((r, g, b))

    st.markdown(f"**Detected Color:** {color_name}")
    st.markdown(f"**RGB Values:** ({r}, {g}, {b})")

    # Show color as a filled box
    st.markdown(
        f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});'></div>",
        unsafe_allow_html=True
    )
else:
    st.write("Please upload an image to get started.")
