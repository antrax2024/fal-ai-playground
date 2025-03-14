import gradio as gr
import numpy as np


def generate_flux_animation(prompt, num_frames=10, width=512, height=512):
    pass


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

            with gr.Column():
                output_animation = gr.Gallery(
                    label="Generated Animation", show_label=True
                )
                output_text = gr.Textbox(label="Output Information")

    return flux_interface
