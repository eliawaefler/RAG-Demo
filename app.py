# app.py

import streamlit as st
import os
from ingest import vectorize_document

# Streamlit interface
st.title('Document Processing Interface')

input_folder = st.text_input('Input Folder', 'documents')
output_folder = st.text_input('Output Folder', 'processed_docs')
process_button = st.button('Process Documents')

if process_button:
    if not os.path.exists(input_folder):
        st.error(f"The input folder '{input_folder}' does not exist.")
    else:
        os.makedirs(output_folder, exist_ok=True)
        files = os.listdir(input_folder)
        if not files:
            st.warning(f"No files found in the input folder '{input_folder}'.")
        else:
            for filename in files:
                filepath = os.path.join(input_folder, filename)
                try:
                    vectorize_document(filepath, output_folder)
                    st.success(f"Successfully processed {filename}")
                except Exception as e:
                    st.error(f"Failed to process {filename}: {str(e)}")
