import gradio as gr
import numpy as np
import time
from PIL import Image


def generate_flux_animation(prompt, num_frames=10, width=512, height=512):
    """
    Function to generate a flux animation based on a prompt
    In a real application, this would call the FAL-AI flux service
    """
    # This is a placeholder - in a real application, you would call the FAL-AI API
    # For demo purposes, generate simple colored frames
    frames = []
    for i in range(num_frames):
        # Create a simple colored image that changes over time
        r = int((np.sin(i / num_frames * np.pi) + 1) * 127)
        g = int((np.cos(i / num_frames * np.pi) + 1) * 127)
        b = int(((np.sin(i / num_frames * np.pi + np.pi / 2) + 1) * 127))

        # Create an array of the specified size with the RGB values
        img_array = np.ones((height, width, 3), dtype=np.uint8)
        img_array[:, :, 0] = r
        img_array[:, :, 1] = g
        img_array[:, :, 2] = b

        frames.append(img_array)

    return frames, f"Generated {num_frames} frames with prompt: {prompt}"


def create_flux_interface():
    """Creates and returns the flux interface"""

    with gr.Blocks() as flux_interface:
        gr.Markdown("# Flux Animation Generator")
        gr.Markdown("Generate animated content based on text prompts.")

        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="Animation Prompt",
                    placeholder="Describe the animation you want to create...",
                )
                num_frames = gr.Slider(
                    minimum=5, maximum=50, value=10, step=1, label="Number of Frames"
                )
                width = gr.Slider(
                    minimum=256, maximum=1024, value=512, step=64, label="Width"
                )
                height = gr.Slider(
                    minimum=256, maximum=1024, value=512, step=64, label="Height"
                )
                generate_btn = gr.Button("Generate Animation")

            with gr.Column():
                output_animation = gr.Gallery(
                    label="Generated Animation", show_label=True
                )
                output_text = gr.Textbox(label="Output Information")

        generate_btn.click(
            fn=generate_flux_animation,
            inputs=[prompt, num_frames, width, height],
            outputs=[output_animation, output_text],
        )

    return flux_interface
