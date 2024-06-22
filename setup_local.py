
def download_CLIP():
    from transformers import CLIPProcessor, CLIPModel

    # Download the model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", cache_dir="./model_cache")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", cache_dir="./model_cache")


