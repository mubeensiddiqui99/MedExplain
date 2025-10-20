import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os
from gtts import gTTS


#from dotenv import load_dotenv
#load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Streamlit setup ---
st.set_page_config(page_title="🩺 MedExplain Chat", page_icon="💬", layout="centered")
st.title("💬 MedExplain - Your AI Health Report Companion")

st.write("Upload your medical report and chat with your AI doctor to understand it better.")

# --- Sidebar for file upload and language selection ---
with st.sidebar:
    st.header("📄 Upload Report")
    uploaded_file = st.file_uploader("Upload your medical report (PDF)", type=["pdf"])

    language = st.selectbox(
        "Select explanation language:",
        ["English", "Urdu", "Hindi"],
        index=0
    )

# --- Session state to store extracted text and chat history ---
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Extract text from uploaded PDF ---
if uploaded_file and not st.session_state.extracted_text:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = ""

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""

        if not extracted_text.strip():
            st.error("Could not extract text from this PDF. Try another file.")
        else:
            st.session_state.extracted_text = extracted_text
            st.success("✅ Report uploaded and analyzed! You can now start chatting below.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# --- Chat interface ---
if st.session_state.extracted_text:
    st.divider()
    st.subheader("💬 Chat with MedExplain")

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Chat input ---
    user_input = st.chat_input("Ask a question about your report...")

    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your report..."):
                model = genai.GenerativeModel("gemini-2.5-flash")

                prompt = f"""
                You are a friendly medical explanation bot helping users understand their medical reports.
                The report text is below. Respond conversationally to their question in the chosen language.
                Use simple, kind, human-like tone. Avoid jargon.
                Respond in romanized {language} only, unless its English - then repond in normal english.

                --- Report Content ---
                {st.session_state.extracted_text}

                --- User Question ---
                {user_input}
                """

                response = model.generate_content(prompt)
                ai_text = response.text.strip()

                # Display assistant message
                st.markdown(ai_text)

                # Save response in session
                st.session_state.messages.append({"role": "assistant", "content": ai_text})

                # --- Optional: Generate audio ---
                try:
                    tts = gTTS(text=ai_text, lang="en")
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.warning("Could not generate audio output.")

else:
    st.info("👆 Please upload a medical report first to start chatting.")

