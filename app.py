import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Receipt Organizer", layout="centered")
st.title("Smart Receipt to Monthly Excel Organizer")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Receipt", use_container_width=True)
    
    if st.button("Process Receipt"):
        with st.spinner("Analyzing receipt..."):
            try:
                image_bytes = uploaded_file.getvalue()

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[
                        {
                            "inline_data": {
                                "data": image_bytes,
                                "mime_type": uploaded_file.type
                            }
                        },
                        "Extract the receipt details (store name, date, items, total amount) into a clean format."
                    ]
                )

                st.success("Receipt processed successfully!")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error processing image: {e}")