
def download_CLIP():
    from transformers import CLIPProcessor, CLIPModel

    # Download the model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", cache_dir="../clip_model")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", cache_dir="../clip_model")


def download_BLIP():
    from transformers import BlipProcessor, BlipForConditionalGeneration

    # Specify the local directory where you want to save the model and processor
    local_model_dir = "./blip_model"
    
    # Download and save the processor and model locally
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    processor.save_pretrained(local_model_dir)
    
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.save_pretrained(local_model_dir)


