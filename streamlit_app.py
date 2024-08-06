import os
import streamlit as st
import google.generativeai as genai

# --- Load system instruction from a text file ---
def load_system_instruction(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
# --- Google Gemini Setup ---
os.environ["GEMINI_API_KEY"] = st.secrets['GOOGLE_API_KEY']  
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Assuming your system instruction is in a file called 'prompt.txt'
system_instruction = load_system_instruction("prompt.txt")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    system_instruction=system_instruction, 
    #safety_settings="None",
)

chat_session = model.start_chat() 

# --- Streamlit App ---
st.title("Chatbot del General Andrés Avelino Cáceres")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("¿Qué desea preguntarle al General?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chat_session.send_message(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response.text)
