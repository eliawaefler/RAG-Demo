from sentence_transformers import SentenceTransformer
import numpy as np
import json

model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text: str) -> list:
    return model.encode(text).tolist()


def get_embeddings(texts: list[str]) -> dict:
    return {t: get_embedding(t) for t in texts}


def list_to_vecstore(in_file):
    with open(in_file, "r") as f:
        with open(in_file + "_vecstore", "w") as newfile:
            json.dump(get_embeddings(f.readlines()), newfile)


if __name__ == '__main__':
    #list_to_vecstore("kbob")
    emb = get_embedding("Dieser Satz wird vektorisiert.")
    print(len(emb))
