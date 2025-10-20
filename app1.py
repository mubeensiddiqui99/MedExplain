import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os
from gtts import gTTS


# Uncomment for local testing, causing issues in streamlit deployment

#from dotenv import load_dotenv


#load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="MedExplain - AI Health Report Simplifier", page_icon="🩺" , layout="centered")
st.title("🩺 MedExplain - AI Health Report Simplifier")

st.write("Upload your medical report PDF to get a simple, easy-to-understand explanation.")


uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])


language = st.selectbox(
    "Select your preferred language for explanation:",
    ["English", "Urdu", "Hindi"],
    index=0
)


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


                prompt = f"""

                    You are a bot that is meant to help people with low medical and language literacy understand complex medical blood reports, and help them understand what they can do too improve their scores.
                    Explain the following medical report in simple, kind, and realistic language that a layperson can understand.
                    Avoid medical jargon and use a friendly tone.

                    Respond ONLY in plain text (no markdown, no symbols, no formatting).
                    Write your response entirely in the roman version of the following language: {language}.
                    Your response will be used in a text-to-speech application, so ensure it is easy to read aloud.
                    
                    Report content:
                    {extracted_text}
                
                """
              
                if st.button("🧠 Generate Explanation"):
                    with st.spinner("Analyzing your report..."):
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(prompt)
                        ai_text = response.text.strip()


                        # Display response
                        st.subheader("💬 Simple Explanation")
                        st.text_area("AI Response", response.text, height=300)


                        # --- Convert to speech ---
                        with st.spinner("Generating audio..."):
                            tts = gTTS(text=ai_text, lang="en")
                            audio_bytes = io.BytesIO()
                            tts.write_to_fp(audio_bytes)
                            audio_bytes.seek(0)

                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("✅ Audio generated successfully! You can play it above.")

              

    except Exception as e:
        st.error(f"Error reading PDF: {e}")