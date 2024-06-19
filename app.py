# app.py

import streamlit as st
import os
import json
import numpy as np
from transformers import pipeline

# Load vector store
vector_store = {}
docs = {}


# setup.py

import hashlib
import fitz  # PyMuPDF
import docx
import pandas as pd
from PIL import Image
import pytesseract
from transformers import CLIPProcessor, CLIPModel, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

# Initialisieren der Modelle
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

def vectorize_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy().tolist()
    return embeddings


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
