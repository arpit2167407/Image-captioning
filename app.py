# import gradio as gr
# import os
# from captioning import generate_caption
# from dataset import preprocess_image

# def gradio_generate_and_evaluate(image):
#     """
#     Function to generate caption and evaluate it for the uploaded image.
#     Args:
#         image (PIL.Image): The uploaded image.
#     Returns:
#         str: The caption and evaluation results.
#     """
#     # Generate caption for the uploaded image
#     generated_caption = generate_caption(image)
    
#     # As there is no filename in the image object, we can either:
#     # 1. Save the image temporarily to generate a filename, or
#     # 2. Directly skip filename and focus on caption generation and evaluation.
    
#     # If you want to skip filename handling, you can remove the following lines.
#     # For now, let's just generate a temporary filename using a unique identifier.
#     temp_filename = "temp_image.jpg"
#     image.save(temp_filename)  # Save the image temporarily
    
#     # If you have ground truth captions to compare for evaluation, you can load them
#     # Assuming you have a captions file with the ground truth data (e.g., captions.txt)
#     captions_file = "/Users/arpitsharma/cvision/captions.txt"  # Update with actual path
#     with open(captions_file, "r") as f:
#         lines = f.readlines()
    
#     # Parse captions (assuming "image_name\tcaption" format)
#     captions_data = {}
#     for line in lines:
#         parts = line.strip().split("\t")
#         if len(parts) == 2:
#             image_name, caption = parts
#             captions_data[image_name] = caption
    
#     # Evaluate the caption against ground truth (simple exact match evaluation)
#     ground_truth = captions_data.get(temp_filename, "")
#     evaluation_result = "Match" if generated_caption == ground_truth else "No Match"
    
#     # Return the generated caption and evaluation result
#     return f"Generated Caption: {generated_caption}\nEvaluation: {evaluation_result}"

# # Gradio Interface
# title = "Image Captioning and Evaluation"
# description = "Upload an image to generate a caption and evaluate it."

# # Input components
# inputs = gr.Image(type="pil", label="Upload Image")

# # Output component
# outputs = gr.Textbox(label="Caption and Evaluation Result")

# # Interface
# interface = gr.Interface(
#     fn=gradio_generate_and_evaluate,
#     inputs=inputs,
#     outputs=outputs,
#     title=title,
#     description=description,
# )

# if __name__ == "__main__":
#     interface.launch(share=True)


# import gradio as gr
# from PIL import Image
# from captioning import generate_caption  # Assuming generate_caption is your captioning function

# def gradio_generate_caption(image):
#     """
#     Function to generate a caption for the uploaded image.
#     Args:
#         image (PIL.Image): The uploaded image.
#     Returns:
#         str: The generated caption for the image.
#     """
#     if image is None:
#         return "No image provided."

#     # Ensure the image is in the correct format (if needed)
#     if not isinstance(image, Image.Image):
#         try:
#             image = Image.open(image)  # Ensure it's a PIL image
#         except Exception as e:
#             return f"Error loading image: {str(e)}"

#     # Generate caption for the uploaded image
#     generated_caption = generate_caption(image)
    
#     return generated_caption

# # Gradio Interface
# title = "Image Captioning"
# description = "Upload an image to generate a caption."

# # Input components
# inputs = gr.Image(type="pil", label="Upload Image")

# # Output component
# outputs = gr.Textbox(label="Generated Caption")

# # Interface
# interface = gr.Interface(
#     fn=gradio_generate_caption,
#     inputs=inputs,
#     outputs=outputs,
#     title=title,
#     description=description,
# )

# if __name__ == "__main__":
#     interface.launch(share=True)




# import gradio as gr
# from PIL import Image
# from captioning import generate_caption  # Assuming generate_caption is your captioning function
# import nltk
# from nltk.translate.bleu_score import corpus_bleu

# # Download necessary NLTK data for BLEU
# nltk.download('punkt')

# def gradio_generate_and_compare(image, user_caption):
#     """
#     Function to generate a caption for the uploaded image and compare it with the user's input caption.
#     Args:
#         image (PIL.Image): The uploaded image.
#         user_caption (str): The manually input caption.
#     Returns:
#         dict: Generated caption and BLEU score comparing user input with the generated caption.
#     """
#     if image is None:
#         return "No image provided."

#     # Generate caption for the uploaded image
#     generated_caption = generate_caption(image)

#     # Tokenize the captions
#     reference_tokens = user_caption.split()  # Tokenize user's input caption
#     hypothesis_tokens = generated_caption.split()  # Tokenize the generated caption

#     # Calculate BLEU Score
#     bleu_score = corpus_bleu([[reference_tokens]], [hypothesis_tokens])

#     # Collect evaluation results
#     evaluation_results = {
#         "Generated Caption": generated_caption,
#         "User's Caption": user_caption,
#         "BLEU Score": bleu_score
#     }

#     return generated_caption, user_caption, evaluation_results

# # Gradio Interface
# title = "Image Captioning and BLEU Score Evaluation"
# description = "Upload an image to generate a caption, then input your own caption and compare it with the generated one using BLEU score."

# # Input components
# inputs = [
#     gr.Image(type="pil", label="Upload Image"),
#     gr.Textbox(label="Your Caption", placeholder="Enter your own caption here...")
# ]

# # Output components
# outputs = [
#     gr.Textbox(label="Generated Caption"),
#     gr.Textbox(label="Your Caption"),
#     gr.JSON(label="Caption Comparison and BLEU Score")
# ]

# # Interface
# interface = gr.Interface(
#     fn=gradio_generate_and_compare,
#     inputs=inputs,
#     outputs=outputs,
#     title=title,
#     description=description,
# )

# if __name__ == "__main__":
#     interface.launch(share=True,inbrowser=True)





import gradio as gr
from PIL import Image
from captioning import generate_caption  # Assuming generate_caption is your captioning function
import nltk
from nltk.translate.bleu_score import corpus_bleu

# Download necessary NLTK data for BLEU
nltk.download('punkt')

# Function to load captions from captions.txt
def load_captions(file_path):
    """
    Function to load captions from the captions.txt file.
    Assumes the file format is image filename, followed by the caption on the same line.
    """
    captions = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines and lines that don't contain a comma
            line = line.strip()
            if not line or ', ' not in line:
                continue

            try:
                # Try to split by the first comma
                image_filename, caption = line.split(', ', 1)
                captions[image_filename] = caption
            except ValueError:
                print(f"Skipping line: {line}")  # You can log it if needed
    return captions

# Load captions from the file (specify your path to captions.txt here)
captions_file_path = '/Users/arpitsharma/cvision/captions.txt'
captions_dict = load_captions(captions_file_path)

def gradio_generate_and_compare(image, image_filename):
    """
    Function to generate a caption for the uploaded image and compare it with the reference caption.
    Args:
        image (PIL.Image): The uploaded image.
        image_filename (str): The filename of the uploaded image.
    Returns:
        dict: Generated caption and BLEU score comparing reference caption with the generated caption.
    """
    if image is None:
        return "No image provided."

    # Generate caption for the uploaded image
    generated_caption = generate_caption(image)

    # Retrieve the reference caption from the captions dictionary based on the uploaded image filename
    reference_caption = captions_dict.get(image_filename, "No reference caption found for this image")

    # Tokenize the captions
    reference_tokens = reference_caption.split()  # Tokenize reference caption
    hypothesis_tokens = generated_caption.split()  # Tokenize the generated caption

    # Calculate BLEU Score
    bleu_score = corpus_bleu([[reference_tokens]], [hypothesis_tokens])

    # Collect evaluation results
    evaluation_results = {
        "Generated Caption": generated_caption,
        "Reference Caption": reference_caption,
        "BLEU Score": bleu_score
    }

    return generated_caption, reference_caption, evaluation_results

# Gradio Interface
title = "Image Captioning and BLEU Score Evaluation"
description = "Upload an image and provide the filename to generate a caption, then compare it with the reference caption from the dataset using BLEU score."

# Input components
inputs = [
    gr.Image(type="pil", label="Upload Image"),  # Only ask for image
    gr.Textbox(label="Image Filename", placeholder="Enter image filename (e.g., '998845445.jpg')")  # For selecting the image
]

# Output components
outputs = [
    gr.Textbox(label="Generated Caption"),
    gr.Textbox(label="Reference Caption"),
    gr.JSON(label="Caption Comparison and BLEU Score")
]

# Interface
interface = gr.Interface(
    fn=gradio_generate_and_compare,
    inputs=inputs,
    outputs=outputs,
    title=title,
    description=description,
)

if __name__ == "__main__":
    interface.launch(share=True, inbrowser=True)

