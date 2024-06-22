import json
import os
import numpy as np
from utils.local_embeddings import get_embedding

def get_vector_store(folder_path="C:\\Users\\eliaw\\python projects\\RAG-Demo\\processed_docs"):
    my_vector_store = {}
    my_docs = {}
    my_texts = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as file:
                j_doc = json.load(file)
                for item in j_doc["data"]:
                    key = f"{j_doc['name']}_{item['id']}"
                    my_vector_store[key] = np.array(item['vektor'])
                    my_docs[key] = j_doc['name']
                    my_texts[key] = item['text']
    return [my_vector_store, my_docs, my_texts]


def find_best_chunks(vectorstore, query_vec, top_k=5):
    similarities = {key: np.dot(query_vec, vec) for key, vec in vectorstore.items()}
    best_chunks = sorted(similarities, key=similarities.get, reverse=True)[:top_k]
    return best_chunks


if __name__ == '__main__':
    vecs, docs, texts = get_vector_store()
    print(vecs[list(vecs.keys())[0]])
    print(docs[list(docs.keys())[0]])
    print(find_best_chunks(vectorstore=vecs, query_vec=get_embedding("chinesisch")))

