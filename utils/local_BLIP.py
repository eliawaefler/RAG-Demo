"""
THIS SCRIPT INTERACTS WITH THE DOWNLOADED BLIP MODEL
IT IS NOT USED TO GENERATE TEXT DESCRIPTIONS FOR AN IMAGE.
THE BLIP MODEL MUST BE LOCATED IN THE SAME DIR AS THIS SCRIPT
"""

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


def describe_image(image):
    local_model_dir = "blip_model"

    # Load the processor and model from the local directory
    processor = BlipProcessor.from_pretrained(local_model_dir)
    model = BlipForConditionalGeneration.from_pretrained(local_model_dir)

    # Process the image
    inputs = processor(image, return_tensors="pt")

    # Generate the text description
    with torch.no_grad():
        outputs = model.generate(**inputs)
        description = processor.decode(outputs[0], skip_special_tokens=True)

    return description


if __name__ == '__main__':
    image = Image.open("../data/synthetic//2//Fachkonzepte Heizung oder Lüftung oder Klima oder Sanitär_sample.png")  # Replace with your image path
    print(describe_image(image=image))
