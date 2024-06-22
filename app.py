# app.py

import streamlit as st
import os
import json
import numpy as np
from utils.local_embeddings import get_embedding
from transformers import pipeline
from utils.RAG import get_vector_store, find_best_chunks
from utils.local_LLM import mistral_complete


st.title("Retrieval-Augmented Generation (RAG) App")

vector_store, docs = get_vector_store()



# Load Hugging Face token from Streamlit secrets
hf_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

# Main page layout
query = st.text_input("Ask a question:")
if query:
    query_vec = get_embedding(query)[0]
    best_chunks = find_best_chunks(query_vec)

    # Dynamic prompt creation
    context = "\n\n".join([f"Chunk {i+1}: {vector_store[chunk]}" for i, chunk in enumerate(best_chunks)])
    prompt = f"Answer the user's question using the following information:\n\n{context}\n\nQuestion: {query}\nAnswer:"

    # Generate response
    response = llm(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']

    # Display conversation
    st.write(f"**Query:** {query}")
    st.write(f"**Answer:** {response}")

    # Display most relevant document
    best_doc = docs[best_chunks[0]]
    doc_filepath = os.path.join("documents", best_doc)
    if best_doc.lower().endswith('.pdf'):
        with fitz.open(doc_filepath) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            st.sidebar.write(f"**Most Relevant Document:** {best_doc}")
            st.sidebar.write(text)
    elif best_doc.lower().endswith('.docx'):
        doc = docx.Document(doc_filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.sidebar.write(f"**Most Relevant Document:** {best_doc}")
        st.sidebar.write(text)
    elif best_doc.lower().endswith('.xlsx'):
        dfs = pd.read_excel(doc_filepath, sheet_name=None)
        for sheet_name, df in dfs.items():
            st.sidebar.write(f"**Sheet: {sheet_name}**")
            st.sidebar.write(df)
    elif best_doc.lower().endswith(('.jpg', '.png', '.jpeg')):
        image = Image.open(doc_filepath)
        st.sidebar.write(f"**Most Relevant Document:** {best_doc}")
        st.sidebar.image(image)
    elif best_doc.lower().endswith('.txt'):
        with open(doc_filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            st.sidebar.write(f"**Most Relevant Document:** {best_doc}")
            st.sidebar.write(text)
