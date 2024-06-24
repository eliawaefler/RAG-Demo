"""
THIS SCRIPT CAN BE USED TO DOWNLOAD CLIP AND BLIP MODELS.
FOR MISTRAL, LM STUDIO IS USED
"""


def download_CLIP():
    from transformers import CLIPProcessor, CLIPModel

    # Specify the local directory where you want to save the model and processor
    clip_cache_dir = "./clip_model"

    # Download the model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", cache_dir=clip_cache_dir)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", cache_dir=clip_cache_dir)

    # Explicitly save the downloaded model and processor locally to ensure all files are stored
    model.save_pretrained(clip_cache_dir)
    processor.save_pretrained(clip_cache_dir)


def download_BLIP():
    from transformers import BlipProcessor, BlipForConditionalGeneration

    # Specify the local directory where you want to save the model and processor
    blip_cache_dir = "./blip_model"

    # Download and save the processor and model locally
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    processor.save_pretrained(blip_cache_dir)

    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.save_pretrained(blip_cache_dir)


download_BLIP()
