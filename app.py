# app.py

import streamlit as st
import os

import utils.local_CLIP
from utils.local_embeddings import get_embedding
from utils.RAG import get_text_vector_store, get_img_vector_store, find_best_chunks
from utils.local_LLM import *
from utils.openai_handler import gpt4_new
import fitz
from PIL import Image
import docx
import pandas as pd
import requests
from utils.local_CLIP import *
from transformers import CLIPProcessor, CLIPModel
#model = CLIPModel.from_pretrained("./utils/clip_model")
#processor = CLIPProcessor.from_pretrained("./utils/clip_model")


def find_file(root_dir, file_name):
    """
    Search for a file within a directory and all its subdirectories.

    Parameters:
    - root_dir (str): The root directory to start the search from.
    - file_name (str): The name of the file to find.

    Returns:
    - str: The path to the file if found, otherwise None.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if file_name in filenames:
            return os.path.join(dirpath, file_name)
    return None


def internet_connection() -> bool:
    try:
        if requests.get('http://www.google.com').status_code == 200:
            return True
        else:
            return False
    except:
        return False


def main():
    # innit sessionstate
    if "internet_available" not in sst:
        sst.internet_available = internet_connection()
    if "mistral" not in sst:
        sst.mistral = False

    # Main page
    st.title("Komplett lokale Retrieval-Augmented Generation (RAG) App")
    query = st.text_input("Frage etwas:")
    if st.toggle("openai/mistral"):
        sst["mistral"] = True
        st.write("mistral geladen: " + str(mistral_connection()))
    else:
        sst["mistral"] = False
        st.write("internet verbunden: " + str(internet_connection()))
    if query:
        with st.spinner("processing"):
            query_text_vec = get_embedding(query)
            query_img_vec = embedd_text(query)
            best_chunks = find_best_chunks(vectorstore=txt_vecs, query_vec=query_text_vec)
            #best_imgs = find_best_chunks(vectorstore=img_vecs, query_vec=query_img_vec)
            #best_chunks = [] #combine with imgs
            context = "\n\n".join([f"Chunk {i+1}: {texts[chunk]}" for i, chunk in enumerate(best_chunks)])
            prompt = f"Beantworte die folgende Frage auf Deutsch, mit den Informationen:" \
                     f"\n\n{context}\n\nFrage: {query}\nAntwort:"
        l, r = st.columns([1, 1])
        with r:
            # Display most relevant document
            best_doc = docs[best_chunks[0]]

            #doc_filepath = os.path.join("data\\documents", best_doc)
            doc_filepath = find_file("data\\documents", best_doc)
            if best_doc.lower().endswith('.pdf'):
                with fitz.open(doc_filepath) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    st.write(f"**Most Relevant Document:** {best_doc}")
                    st.write(text)
            elif best_doc.lower().endswith('.docx'):
                doc = docx.Document(doc_filepath)
                text = "\n".join([para.text for para in doc.paragraphs])
                st.write(f"**Most Relevant Document:** {best_doc}")
                st.write(text)
            elif best_doc.lower().endswith('.xlsx'):
                dfs = pd.read_excel(doc_filepath, sheet_name=None)
                for sheet_name, df in dfs.items():
                    st.write(f"**Sheet: {sheet_name}**")
                    st.write(df)
            elif best_doc.lower().endswith(('.jpg', '.png', '.jpeg')):
                image = Image.open(doc_filepath)
                st.write(f"**Most Relevant Document:** {best_doc}")
                st.image(image)
            elif best_doc.lower().endswith('.txt'):
                with open(doc_filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    st.write(f"**Most Relevant Document:** {best_doc}")
                    st.write(text)
        with l:
            if sst.mistral:
                if mistral_connection():
                    st.write("using mistral")
                    response = mistral_complete(prompt)
                else:
                    st.write("mistral ist nicht geladen.")
                    response = False
            elif internet_connection():
                st.write("using GPT4")
                response = gpt4_new(prompt)
            else:
                st.write("bitte lade mistral lokal oder verbinde mit dem internet")
                response = False
            # Display conversation
            st.write(f"**Query:** {query}")
            st.write(f"**Answer:** {response}")


sst = st.session_state
txt_vecs, docs, texts = get_text_vector_store()
img_vecs, imgs = get_img_vector_store()
def debug_me():
    a = []
    for l in list(txt_vecs.keys()):
        a.append(len(txt_vecs[l]))
    b = []
    for l in list(img_vecs.keys()):
        b.append(len(img_vecs[l]))
    print("text")
    print(len(list(txt_vecs.keys())))
    print([a])
    print(len(utils.local_embeddings.get_embedding("hello")))

    print("")
    print("imgs")
    print(len(list(img_vecs.keys())))
    print(b)
    print(len(utils.local_CLIP.embedd_text("hello")))
if __name__ == '__main__':
    main()