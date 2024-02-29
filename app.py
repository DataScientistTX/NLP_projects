import streamlit as st
import random
import time
import os
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

api_key = st.sidebar._text_input("OPEN API KEY", "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")

def save_api_key(api_key):
    # Set the environment variable
    os.environ["OPENAI_API_KEY"] = api_key

# Save the API key to an environment variable
if st.sidebar.button("Save API Key"):
    save_api_key(api_key)
    st.success("API Key saved successfully!")


def save_uploaded_file(uploaded_file, save_dir):
    with open(os.path.join(save_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is None:
    st.write("Please upload a document for model training")

if uploaded_file is not None:
    save_dir = "data"  #  your desired directory
    os.makedirs(save_dir, exist_ok=True)
    save_uploaded_file(uploaded_file, save_dir)
    st.success(f"File saved successfully at {save_dir}/{uploaded_file.name}")

    #if uploaded file is not None
    # check if storage already exists
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    # Either way we can now query the index
    query_engine = index.as_query_engine()

    # Streamed response emulator

    st.title("PXD Chatbot Demo")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        response = query_engine.query(prompt)
        #st.write(str(response))
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.write(str(response))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})