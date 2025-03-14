import gradio as gr
import numpy as np
from PIL import Image


def inpaint_image(input_image, mask_image, prompt):
    """
    Function to perform inpainting on an image
    In a real application, this would call the FAL-AI inpainting service
    """
    # This is a placeholder - in a real application, you would call the FAL-AI API
    # For demo purposes, just return the original image
    result = input_image
    return result, f"Processed with prompt: {prompt}"


def create_inpainting_interface():
    """Creates and returns the inpainting interface"""

    with gr.Blocks() as inpainting_interface:
        gr.Markdown("# Image Inpainting")
        gr.Markdown(
            "Upload an image, create a mask, and provide a prompt to inpaint the masked area."
        )

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Original Image", type="numpy")
                mask_image = gr.Image(
                    label="Mask (Draw on areas to inpaint)",
                    type="numpy",
                )
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe what should appear in the masked area...",
                )
                process_btn = gr.Button("Process Inpainting")

            with gr.Column():
                output_image = gr.Image(label="Result")
                output_text = gr.Textbox(label="Output Information")

        process_btn.click(
            fn=inpaint_image,
            inputs=[input_image, mask_image, prompt],
            outputs=[output_image, output_text],
        )

    return inpainting_interface
