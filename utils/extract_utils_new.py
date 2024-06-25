"""
Extracting Text and Images from XLSX, DOXC AND PDF
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from docx import Document
import local_LLM
from docx2txt import process as docx_process
from uuid import uuid4
from PIL import Image
import io
import fitz  # PyMuPDF
from pdf2image import convert_from_path

def process_table(df: pd.DataFrame) -> str:
    """Generate a summary from a DataFrame."""
    table_csv = df.to_csv(index=False)
    prompt = ("Analyze the following table and provide a summary of key information:\n\n"
              f"{table_csv}\n\n"
              "Include important insights, trends, and notable data points.")
    # Placeholder for GPT-4 API call:
    response = local_LLM.mistral_complete(prompt)  # Replace with actual API call
    return response

def save_image(img: Image, path: str) -> None:
    """Save an image to the specified path."""
    img.save(path, format='PNG')

def chunk_text(text: str, chunk_size: int = 1000) -> list:
    """Split text into specified size chunks."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def extract_images_from_pdf(page, doc, output_dir, page_num):
    """Extract and save images from a PDF page."""
    images = page.get_images(full=True)
    image_data = []
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        img = Image.open(io.BytesIO(image_bytes))
        img_path = os.path.join(output_dir, f'page{page_num}_img{img_index}.png')
        save_image(img, img_path)
        image_data.append({
            "title": f'Image from page {page_num}',
            "path": img_path,
            "text": ""
        })
    return image_data

def extract_text_from_pdf(page):
    """Extract text from a PDF page."""
    return page.get_text()

def process_pdf(filepath: str, output_dir: str) -> dict:
    """Process a PDF file and extract information."""
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        return {"error": f"Failed to open PDF: {str(e)}"}

    filename = os.path.basename(filepath)
    json_data = {
        "name": filename,
        "unique_id": str(uuid4()),
        "data": []
    }

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = extract_text_from_pdf(page)
        images = extract_images_from_pdf(page, doc, output_dir, page_num)

        json_data["data"].extend(images)
        json_data["data"].append({
            "title": f'Text from page {page_num}',
            "text": text
        })

    doc.close()
    return json_data

def extract_images_from_docx(doc, filepath, output_dir):
    """Extract and save images from a DOCX document."""
    image_data = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            img_path = os.path.join(output_dir, f'{rel.target_ref}.png')
            img = docx_process(filepath, img_path)
            save_image(img, img_path)
            image_data.append({
                "title": f'Image from {os.path.basename(filepath)}',
                "path": img_path,
                "text": ""
            })
    return image_data

def process_docx(filepath: str, output_dir: str) -> dict:
    """Process a DOCX file and extract information."""
    try:
        doc = Document(filepath)
    except Exception as e:
        return {"error": f"Failed to open DOCX: {str(e)}"}

    filename = os.path.basename(filepath)
    json_data = {
        "name": filename,
        "unique_id": str(uuid4()),
        "data": []
    }

    text = "\n".join([para.text for para in doc.paragraphs])
    images = extract_images_from_docx(doc, filepath, output_dir)

    json_data["data"].extend(images)
    json_data["data"].append({
        "title": f'Text from {filename}',
        "text": text
    })

    return json_data

def process_xlsx(filepath: str, output_dir: str) -> dict:
    """Process an XLSX file and extract table images and summaries."""
    try:
        xls = pd.ExcelFile(filepath)
    except Exception as e:
        return {"error": f"Failed to open XLSX: {str(e)}"}

    filename = os.path.basename(filepath)
    json_data = {
        "name": filename,
        "unique_id": str(uuid4()),
        "data": []
    }

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        summary = process_table(df)
        json_data["data"].append({
            "title": f'Summary of {sheet_name}',
            "text": summary
        })

    return json_data

def extract_info(filepath: str, output_dir: str) -> dict:
    """Extract information based on file type."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if filepath.endswith('.pdf'):
        return process_pdf(filepath, output_dir)
    elif filepath.endswith('.docx'):
        return process_docx(filepath, output_dir)
    elif filepath.endswith('.xlsx'):
        return process_xlsx(filepath, output_dir)
    else:
        return {"error": "Unsupported file type"}
