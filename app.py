import streamlit as st
# Assuming reco_main.py is in the same directory and contains the suggest_movie function
from reco_main import suggest_movie

# --- 1. Basic Setup and Title ---
st.set_page_config(page_title="Movie Suggestion Bot", page_icon="🎬")
st.title("🎬 AI Movie Suggestions")

# --- 2. Initialize Chat History ---
# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming initial message from the bot
    st.session_state.messages.append({"role": "assistant", "content": "Hello! Tell me your favorite movie, and I'll recommend similar titles."})

# --- 3. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 4. Handle New User Input ---
query = st.chat_input("Enter your favorite movie name here...")

if query:
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # Display a spinner and generate response
    with st.chat_message("assistant"):
        with st.spinner(f"Finding recommendations for '{query}'..."):
            # Call the recommendation function
            try:
                response_text = suggest_movie(query)
                st.write(response_text)
                # Add the assistant's response to the history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                error_message = f"An error occurred: Could not generate content. Please check your API key and network connection. ({e})"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# A friendly footer (optional, but good for UX)
st.markdown("---")
