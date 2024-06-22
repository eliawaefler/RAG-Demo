import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load the model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", cache_dir="../model_cache")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", cache_dir="../model_cache")


def describe_image(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.get_image_features(**inputs)

    # Find the most similar text descriptions in the model's vocabulary
    descriptions = [
        "a photo of a cat", "a photo of a dog", "a photo of a person", "a photo of a car",
        "a photo of a building", "a photo of nature", "a photo of food", "a photo of an animal"
    ]
    text_inputs = processor(text=descriptions, return_tensors="pt", padding=True)
    text_outputs = model.get_text_features(**text_inputs)

    # Calculate cosine similarity between image and text embeddings
    image_features = outputs.image_embeds
    text_features = text_outputs.text_embeds
    similarities = torch.nn.functional.cosine_similarity(image_features, text_features, dim=1)

    # Get the most similar description
    best_match = descriptions[torch.argmax(similarities).item()]

    return best_match


if __name__ == '__main__':
    image_path = "../img.png"  # Replace with the path to your image
    description = describe_image(image_path)
    print("Description:", description)
