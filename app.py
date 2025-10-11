import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="MedExplain - AI Health Report Simplifier", page_icon="🩺" , layout="centered")
st.title("🩺 MedExplain - AI Health Report Simplifier")

st.write("Upload your medical report PDF to get a simple, easy-to-understand explanation.")


uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])


if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = ''

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""

        if not extracted_text.strip():
                    st.error("Could not extract readable text from this PDF. Please try another file.")
        else:
              st.subheader("Extracted Text Preview:")
              st.text_area("Extracted content", extracted_text[:2000], height=200)

              
        



    except Exception as e:
        st.error(f"Error reading PDF: {e}")