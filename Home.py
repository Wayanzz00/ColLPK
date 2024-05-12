import streamlit as st
import base64
import requests
from streamlit_lottie import st_lottie  # Assuming you're using a Streamlit extension for Lottie animations


def img_to_base64(image_path):
    """Convert image to base64"""
    with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    # Load image and convert to base64
img_path = "imgs/icon_aka.png"  # Replace with the actual image path
img_base64 = img_to_base64(img_path)
st.sidebar.markdown(
    f'<img src="data:image/png;base64,{img_base64}" style="width: 100%; height: auto;">',
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.header("~~~ PROJECT LPK ~~~")

# Create two columns
col1, col2 = st.columns([1, 2])

with col1 :
    st.title (" ")
    st.title (" ")
    st.title("TITRIMETRI")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/Alkalimetri.py", label="Alkalimetri", icon="1️⃣")
    st.page_link("pages/Asidimetri.py", label="Asidimetri", icon="2️⃣")
    st.page_link("pages/Permanganometri.py", label="Permanganometri", icon="3️⃣")
    st.page_link("pages/Iodometri.py", label="Iodometri", icon="4️⃣")
    st.page_link("pages/Kompleksometri.py", label="Kompleksometri", icon="5️⃣")
    st.page_link("http://www.google.com", label="Google", icon="🌎")

# Define the URL of the Lottie file (JSON format)
lottie_url = "https://lottie.host/cbcd7e7b-3119-45a2-862a-858ba07d3e39/TlOccKrpDV.json"

# Function to load Lottie animation from URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the Lottie animation
lottie_json = load_lottie_url(lottie_url)

# Display the Lottie animation
with col2 :
    if lottie_json is not None:
        st_lottie(lottie_json)
    else:
        st.write("Failed to load Lottie animation.")
    
