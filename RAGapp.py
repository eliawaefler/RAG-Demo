# app.py

import streamlit as st
import os
import json
import numpy as np
from setup import vectorize_text
from transformers import pipeline

# Load vector store
vector_store = {}
docs = {}

st.title("Retrieval-Augmented Generation (RAG) App")

# Load all JSON files from processed_docs folder
processed_docs_folder = "processed_docs"
for filename in os.listdir(processed_docs_folder):
    filepath = os.path.join(processed_docs_folder, filename)
    if filename.endswith('.json'):
        with open(filepath, 'r', encoding='utf-8') as file:
            doc = json.load(file)
            for item in doc["data"]:
                key = f"{doc['name']}_{item['id']}"
                vector_store[key] = np.array(item['vektor'])
                docs[key] = doc['name']

# Function to find the best matching chunks
def find_best_chunks(query_vec, top_k=5):
    similarities = {key: np.dot(query_vec, vec) for key, vec in vector_store.items()}
    best_chunks = sorted(similarities, key=similarities.get, reverse=True)[:top_k]
    return best_chunks

# Load LLM
llm = pipeline("text-generation", model="gpt-3.5-turbo")

# Main page layout
query = st.text_input("Ask a question:")
if query:
    query_vec = vectorize_text(query)[0]  # Assuming single vector for the query
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
