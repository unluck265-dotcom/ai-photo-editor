import streamlit as st
from PIL import Image
import io
import requests

# AI Model URL (InstructPix2Pix - Text command se photo change karne ke liye)
API_URL = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"

# Page Configuration
st.set_page_config(page_title="AI Photo Customizer", page_icon="🎨", layout="centered")

st.title("🎨 AI Photo Customizer")
st.write("Apni photo upload karein aur text prompt likhkar kapde, hairstyle, background ya accessories badlein!")

# Sidebar me API Key Input
st.sidebar.header("🔑 API Setup")
api_key = st.sidebar.text_input("Apni Hugging Face API Key daalein:", type="password")

st.sidebar.markdown("""
---
**⚡ Kaise Use Karein?**
1. Hugging Face se apni free API Key banakar yahan dalein.
2. Apni photo upload karein.
3. English me prompt likhein (e.g. *change shirt to red jacket*, *add black sunglasses*).
4. **Magic Generate** par click karein.
""")

# Photo Upload Area
uploaded_file = st.file_uploader("📷 Photo Upload Karein (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Original Image Show Karna
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Original Photo", use_column_width=True)

    # Text Prompt Input
    prompt = st.text_input(
        "✏️ Kya badalna chahte hain? (English Prompt):",
        placeholder="Jaise: Change clothes to blue denim jacket and add sunglasses"
    )

    if st.button("✨ Magic Generate"):
        if not api_key:
            st.error("⚠️ Kripya pehle Sidebar me apni API Key enter karein!")
        elif not prompt:
            st.warning("⚠️ Kripya ek prompt likhein ki photo me kya change karna hai.")
        else:
            with st.spinner("⏳ AI aapki photo edit kar raha hai... Please wait 10-20 seconds!"):
                try:
                    # Photo ko Bytes me convert karna
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
                    img_bytes = img_byte_arr.getvalue()

                    headers = {"Authorization": f"Bearer {api_key}"}

                    # API Call
                    response = requests.post(
                        API_URL,
                        headers=headers,
                        data=img_bytes,
                        params={"prompt": prompt}
                    )

                    if response.status_code == 200:
                        result_image = Image.open(io.BytesIO(response.content))
                        st.success("🎉 Successfully Generated!")
                        st.image(result_image, caption="AI Edited Photo", use_column_width=True)
                    else:
                        st.error("❌ Process karne me dikkat aayi. Check karein ki API Key sahi hai ya thodi der baad try karein.")
                except Exception as e:
                    st.error(f"Error: {e}")
