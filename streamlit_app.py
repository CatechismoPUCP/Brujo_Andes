import os
import streamlit as st
import google.generativeai as genai

# --- Load system instruction from a text file ---
def load_system_instruction(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"File di istruzioni di sistema non trovato: {file_path}")
        return ""  # Return an empty string, or handle as appropriate
    except Exception as e:
        st.error(f"Errore durante il caricamento delle istruzioni di sistema: {e}")
        return ""

# --- Google Gemini Setup ---
def configure_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Errore nella configurazione di Gemini: {e}")
        return False


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


# --- Streamlit App ---
st.title("Chatbot Asistente de Psicologia")

# API Key Input
api_key = st.text_input("Inserisci la tua Google API Key:", type="password")

# Initialize session state for messages and model only if API key is provided and valid
if api_key:
    if configure_gemini(api_key):
        # Assuming your system instruction is in a file called 'prompt.txt'
        system_instruction = load_system_instruction("prompt.txt")
        if system_instruction:  # Only proceed if the system instruction loaded
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction=system_instruction,
            )
            chat_session = model.start_chat()
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Get user input
            if prompt := st.chat_input("¿Qué desea preguntarle al ayudante?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                     st.markdown(prompt)
                try:
                    response = chat_session.send_message(prompt)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response.text}
                    )
                    # Display assistant response
                    with st.chat_message("assistant"):
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Errore durante l'invio del messaggio: {e}")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"Si è verificato un errore: {e}"}
                    )
    #removed else, it's implicitly handled by the main if

else:
    st.warning("Per favore, inserisci una Google API Key valida per iniziare.")
