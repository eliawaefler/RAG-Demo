import os
import json
from PIL import Image
import local_embeddings
import local_CLIP


def embed_data_in_folder(folder_path):
    # Loop over each file in the specified folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            # Construct full file path
            json_path = os.path.join(folder_path, file_name)
            # Open and load the JSON file
            with open(json_path, 'r') as file:
                data = json.load(file)

            # Process each item in the "data" list of the JSON
            for item in data['data']:
                # Check if the entry is an image
                if 'path' in item and item['path'].endswith('.png'):
                    image_path = os.path.join(folder_path, item['path'].replace('\\', '/').split('/')[-1])
                    try:
                        image = Image.open(image_path)
                        # Embed the image and update the 'vektor' field
                        item['vektor'] = local_CLIP.embedd_image(image)
                    except FileNotFoundError:
                        print(f"Image file not found: {image_path}")

                # Check if the entry is text
                elif item['text']:
                    # Embed the text and update the 'vektor' field
                    item['vektor'] = local_embeddings.get_embedding(item['text'])

            # Write the updated data back to the JSON file
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=4)


embed_data_in_folder('../data/processed_docs')
