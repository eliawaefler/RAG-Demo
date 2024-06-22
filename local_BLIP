import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Specify the local directory where the model and processor are saved
local_model_dir = ".model_cache/blip_model"

# Load the processor and model from the local directory
processor = BlipProcessor.from_pretrained(local_model_dir)
model = BlipForConditionalGeneration.from_pretrained(local_model_dir)

# Load an image
image = Image.open("your_image.jpg")  # Replace with your image path

# Process the image
inputs = processor(images=image, return_tensors="pt")

# Generate the text description
with torch.no_grad():
    outputs = model.generate(**inputs)
    description = processor.decode(outputs[0], skip_special_tokens=True)

print(description)
