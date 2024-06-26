"""
THIS SCRIPT INTERACTS WITH THE DOWNLOADED CLIP MODEL
IT IS USED TO GENERATE EMBEDDINGS FOR IMAGES AND TEXT IN THE SAME VECTORSPACE.
THE CLIP MODEL MUST BE LOCATED IN THE SAME DIR AS THIS SCRIPT
"""

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load the model and processor
#"openai/clip-vit-base-patch32", cache_dir=
model = CLIPModel.from_pretrained("./utils/clip_model")
processor = CLIPProcessor.from_pretrained("./utils/clip_model")

def embedd_image(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.get_image_features(**inputs)
    return outputs[0].tolist()  # Return the SINGLE IMAGE embedding


def embedd_text(text):
    # Process the text input to prepare it for the model
    inputs = processor(text=[text], return_tensors="pt", padding=True)  # Wrap text in a list for batch processing
    outputs = model.get_text_features(**inputs)
    # Access the first element of the batch, convert the tensor to a list
    return outputs[0].tolist()  # Access the vector for the single text in


if __name__ == '__main__':
    image_path = "../data/synthetic/2/Fachkonzepte Elektrotechnik_sample.png"  # Replace with the path to your image
    image = Image.open(image_path)

    query = embedd_image(image=image)
    store = {e: embedd_text(e) for e in ["photo of nature", "painting by davinchi", "screenshot on laptop",
                                      "sketch by architect", "diagramm in MS visio"]}
    from utils.RAG import *
    print(find_best_chunks(store, query_vec=query, top_k=1))
    #print("Description:", description)
