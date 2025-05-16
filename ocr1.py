import streamlit as st
import openai
import base64
import os

# Load API key from environment variable (set OPENAI_API_KEY in your env)
openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

st.title("Invoice Extraction")

uploaded_file = st.file_uploader("Upload an invoice image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read image bytes
    image_bytes = uploaded_file.read()
    image_data = encode_image(image_bytes)

    prompt_text = "Extract the details from this invoice:\n"

    with st.spinner("Processing invoice."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI that accurately extracts structured data from invoices."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                        ]
                    }
                ]
            )
            result = response.choices[0].message.content
            st.subheader("Extracted Invoice Details:")
            st.text(result)
        except Exception as e:
            st.error(f"Error processing image: {e}")
