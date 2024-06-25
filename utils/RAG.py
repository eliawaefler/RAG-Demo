import json
import os
import numpy as np
import utils.local_embeddings

def get_text_vector_store(folder_path="C:\\Users\\eliaw\\python projects\\RAG-Demo\\data\\processed_docs"):
    my_text_vectors = {}
    my_docs = {}
    my_texts = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as file:
                j_doc = json.load(file)
                for item in j_doc["data"]:
                    if 'path' in item and item['path'].endswith('.png'):
                        pass
                    else:
                        key = f"{j_doc['name']}_{item['id']}"
                        my_text_vectors[key] = np.array(item['vektor'])
                        my_docs[key] = j_doc['name']
                        my_texts[key] = item['text']
    return [my_text_vectors, my_docs, my_texts]


def get_img_vector_store(folder_path="C:\\Users\\eliaw\\python projects\\RAG-Demo\\data\\processed_docs"):
    my_img_vectors = {}
    my_imgs = {}
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as file:
                j_doc = json.load(file)
                for item in j_doc["data"]:
                    if 'path' in item and item['path'].endswith('.png'):
                        key = f"{j_doc['name']}_{item['id']}"
                        my_img_vectors[key] = np.array(item['vektor'])
                        my_imgs[key] = item['path']
                    else:
                        pass
    return [my_img_vectors, my_imgs]


def find_best_chunks(vectorstore, query_vec, top_k=5):
    similarities = {key: np.dot(query_vec, vec) for key, vec in vectorstore.items()}
    best_chunks = sorted(similarities, key=similarities.get, reverse=True)[:top_k]
    return best_chunks


if __name__ == '__main__':
    vecs, docs, texts = get_text_vector_store()
    print(vecs[list(vecs.keys())[0]])
    print(docs[list(docs.keys())[0]])
    print(find_best_chunks(vectorstore=vecs, query_vec=utils.local_embeddings.get_embedding("chinesisch")))

