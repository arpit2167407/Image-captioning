# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration

# # Initialize BLIP model and processor
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# def generate_caption(image):
#     """
#     Generate a caption for the given image using the BLIP model.
#     Args:
#         image (PIL.Image): Input image.
#     Returns:
#         str: Generated caption.
#     """
#     inputs = processor(images=image, return_tensors="pt")
#     output_ids = model.generate(inputs["pixel_values"])
#     caption = processor.decode(output_ids[0], skip_special_tokens=True)
#     return caption

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_caption(image):
    """
    Generate a caption for the given image using the BLIP model.
    Args:
        image (PIL.Image): Input image.
    Returns:
        str: Generated caption.
    """
    if image is None:
        return "No image provided."
    
    # Ensure image is a PIL image if it is passed as file path or raw bytes
    if not isinstance(image, Image.Image):
        try:
            image = Image.open(image)  # If it's a file path or binary data, load it as a PIL image
        except Exception as e:
            return f"Error loading image: {str(e)}"
    
    # Process the image and generate the caption
    try:
        inputs = processor(images=image, return_tensors="pt")
        output_ids = model.generate(inputs["pixel_values"])
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"Error generating caption: {str(e)}"
