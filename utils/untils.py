import openpyxl
import openai_handler
import time
import json
from local_embeddings import get_embedding
from local_CLIP import embedd_text
import json
import os
import numpy as np


def load_classes(class_type):
    with open(f"../data/classes/{class_type}.json", 'r') as file:
        return json.load(file)["data"]


def dot_product(vec1, vec2):
    return np.dot(vec1, vec2)


def classify_document(document, categories, disziplines, doctypes):
    document["hauptkategorie"] = classify_item(document, categories, "bildvektor", "vektor")
    document["disziplin"] = classify_item(document, disziplines, "bildvektor", "vektor")
    document["doctype"] = classify_item(document, doctypes, "bildvektor", "vektor")
    return document


def classify_item(document, classes, clipv_key, bildvektor_key):
    max_score = -float('inf')
    best_class = None

    for cls in classes:
        score_clipv = dot_product(document["data"][0][clipv_key], cls["CLIPV"])
        score_bildvektor = dot_product(document["data"][0][bildvektor_key], cls["LLMV"])
        score = score_clipv + score_bildvektor

        if score > max_score:
            max_score = score
            best_class = cls

    if best_class:
        if not np.allclose(dot_product(document["data"][0]["vektor"], best_class["LLMV"]), 0.1) or not np.allclose(
                dot_product(document["data"][0]["bildvektor"], best_class["CLIPV"]), 0.1):
            print(f"Discrepancy found in document {document['name']} for class {best_class['NAME']}")

    return best_class["CODE"] if best_class else None


def process_documents(folder):
    categories = load_classes("categories")
    disziplines = load_classes("disziplines")
    doctypes = load_classes("doctypes")

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r') as file:
                document = json.load(file)
                classified_document = classify_document(document, categories, disziplines, doctypes)
                save_classified_document(classified_document, folder, filename)


def save_classified_document(document, folder, filename):
    with open(os.path.join(folder, filename), 'w') as file:
        json.dump(document, file, indent=4)


def classify_all_documents():
    haupt_folder = "../data/synth_processed_docs/haupt"
    mittel_folder = "../data/synth_processed_docs/mittel"

    process_documents(haupt_folder)
    process_documents(mittel_folder)


def vectorize_classes_from_json(file_path):
    """
    used to create vectors for the classes.
    :param file_path: the json containing the classes
    :return: True if successful
    """
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Iterate through each entry in the "data" list
    for entry in data['data']:
        # Concatenate NAME and DESC
        combined_text = entry['NAME'] + " " + entry['DESC']

        # Use the CLIP_embedd and LLM_embedd functions to get the vectors

        try:
            clip_vector = embedd_text(combined_text)
        except Exception as e:
            print(e)
            print(combined_text)
            clip_vector = []

        llm_vector = get_embedding(combined_text)

        # Add the vectors to the JSON entry
        entry['CLIPV'] = clip_vector  # Ensure the vectors are converted to lists
        entry['LLMV'] = llm_vector

    # Save the updated JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return True


def read_excel_data(filename):
    # Load the workbook and select the specified sheet
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook["Mittelkategorien_ISB"]

    # Lists to store column data
    column_d_data = []
    column_e_data = []

    # Iterate through each row in the sheet
    for row in sheet.iter_rows(min_row=1, min_col=4, max_col=5):
        # Read the values in columns D and E
        d_value = row[0].value
        e_value = row[1].value

        # Add the values to the lists if they are strings
        if isinstance(d_value, str):
            column_d_data.append(d_value)
        if isinstance(e_value, str):
            column_e_data.append(e_value)

    # Return the lists
    return column_d_data, column_e_data


def create_synt_imgs():
    """
    From Folder
    """
    # Example usage
    d_data, e_data = read_excel_data('A4_DokumententypenkatalogKBOB.xlsx')

    for i in range(4, len(d_data)-1):
        openai_handler.img_create(f"Ansicht eines PDF-Dokuments, dass mit Bauen zu tun hat und für den"
                                  f"Gebäudebetrieb relevant ist. das Dokument wird wie "
                                  f"folgt klassifiziert: {d_data[i]} : {e_data[i]}. generiere nur das Dokument.",
                                  download_path=f"..//data//syntetic//2//{d_data[i]}_sample.png")
        time.sleep(30)


if __name__ == '__main__':
    print("read file")

    classify_all_documents()
    #create_synt_imgs()

    #vectorize_classes_from_json('../data/classes/subcategories.json')
