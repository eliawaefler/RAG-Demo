"""
THIS SCRIPT IS USED TO CREATE THE JSON FILES WITH VECTORS
FROM DOCUMENTS. IT CAN BE TESTET WITH THE 'setup_app.py'.
IT CAN INGEST .JPG .PNG .PDF .DOCX .XLSX and .TXT
THE OUTPUT IS ALWAYS A .JSON FILE WHICH WILL BE SAVED TO processed_docs.
THX TO OPENAI, MISTRAL,
"""

import os
import json
import fitz  # PyMuPDF
import docx
import pandas as pd
from PIL import Image
import local_embeddings
import local_BLIP
import local_CLIP
from sha256 import secure_hash


def process_pdf(filepath):
    try:
        doc = fitz.open(filepath)
        text = []
        images = []
        for page in doc:
            text.append(page.get_text())
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                images.append(Image.open(base_image["image"]))
        return "\n".join(text), images
    except Exception as e:
        raise RuntimeError(f"Failed to process PDF: {e}")


def process_docx(filepath):
    try:
        doc = docx.Document(filepath)
        text = [para.text for para in doc.paragraphs]
        return "\n".join(text), []
    except Exception as e:
        raise RuntimeError(f"Failed to process DOCX: {e}")


def process_xlsx(filepath):
    try:
        dfs = pd.read_excel(filepath, sheet_name=None)
        text = []
        for sheet_name, df in dfs.items():
            text.append(df.to_string())
        return "\n".join(text), []
    except Exception as e:
        raise RuntimeError(f"Failed to process XLSX: {e}")


def process_image(filepath):
    try:
        image = Image.open(filepath)
        return "", [image]
    except Exception as e:
        raise RuntimeError(f"Failed to process image: {e}")


def chunk_text(text, chunk_size=1000, overlap=0.2):
    chunks = []
    overlap_size = int(chunk_size * overlap)
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap_size
    return chunks


def vectorize_document(filepath, output_folder="..//data//processed_docs"):
    try:
        filename = os.path.basename(filepath)
        if filename.lower().endswith(('.txt', '.pdf', '.docx', '.xlsx', '.jpg', '.png', '.jpeg')):
            doc = {
                "name": filename,
                "unique_id": secure_hash(filepath),
                "disziplin": "",
                "doctype": "",
                "hauptkategorie": "",
                "kategorie": "",
                "subkategorie": "",
                "data": []
            }
            text = ""
            images = []

            if filename.lower().endswith('.pdf'):
                text, images = process_pdf(filepath)
            elif filename.lower().endswith('.docx'):
                text, images = process_docx(filepath)
            elif filename.lower().endswith('.xlsx'):
                text, images = process_xlsx(filepath)
            elif filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                text, images = process_image(filepath)
            elif filename.lower().endswith('.txt'):
                with open(filepath, 'r') as file:
                    text = file.read()

            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                chunk_vector = local_embeddings.get_embedding(chunk)
                doc["data"].append({
                    "id": i + 1,
                    "text": chunk,
                    "vektor": chunk_vector
                })

            for i, image in enumerate(images):
                description = local_BLIP.describe_image(image)
                doc["data"].append({
                    "id": len(doc["data"]) + 1,
                    "text": description,
                    "vektor": local_embeddings.get_embedding(description),
                    "bildvektor": local_CLIP.embedd_image(image),
                    "titel": f"Bild {i + 1}"
                })

            output_filepath = os.path.join(output_folder, filename + ".json")
            with open(output_filepath, 'w', encoding='utf-8') as f:
                json.dump(doc, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to vectorize document {filepath}: {e}")


def main():
    #input_folder = "..//data//synthetic//mittel"
    input_folder = "..//data//synthetic//mittel"
    #output_folder = "..//data//synth_processed_docs//mittel"
    output_folder = "..//data//synth_processed_docs//mittel"
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        try:
            vectorize_document(filepath, output_folder)
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    print("read file first")
    #vectorize_document("C:\\Users\\eliaw\\python projects\\RAG-
    #Demo\\data\\documents\\ISB-020-U3-C-D-01-V08703-001-000.pdf")
    vectorize_document("../data/documents/testset_small/img.png")
    #vectorize_document("../data/documents/pdf/ISB-020-U3-D-D-01-V08006-002-000.docx")
    #main()
    #ISB-020-U3-C-D-01-V08703-001-000.pdf
