import json
import os
import numpy as np



def get_vector_store(folder_path="processed_docs"):
    my_vector_store = {}
    my_docs = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as file:
                j_doc = json.load(file)
                for item in j_doc["data"]:
                    key = f"{j_doc['name']}_{item['id']}"
                    my_vector_store[key] = np.array(item['vektor'])
                    my_docs[key] = j_doc['name']
    return my_vector_store, my_docs

def find_best_chunks(query_vec, top_k=5):
    similarities = {key: np.dot(query_vec, vec) for key, vec in vector_store.items()}
    best_chunks = sorted(similarities, key=similarities.get, reverse=True)[:top_k]
    return best_chunks
