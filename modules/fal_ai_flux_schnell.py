import gradio as gr
import fal_client
import asyncio

from gradio.events import Dependency


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": 'Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word "FLUX" is painted over it in big, white brush strokes with visible texture.',
            "image_size": "landscape_4_3",
            "num_inference_steps": 4,
            "num_images": 1,
            "enable_safety_checker": True,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    print(f"Result: {result}")

    # Extract only the URLs from the images array
    image_urls = [image["url"] for image in result["images"]]
    print(f"Image URLs: {image_urls}")
    return image_urls

    # return result["images"]


def create_flux_interface() -> gr.Blocks:
    """Creates and returns the flux interface"""
    with gr.Blocks() as flux_interface:
        gr.Markdown(value="# fal-ai/flux/schnell ")
        gr.Markdown(
            value="FLUX.1 [schnell] is a 12 billion parameter flow transformer that generates high-quality images from text in 1 to 4 steps, suitable for personal and commercial use."
        )

        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe the animation you want to create...",
                    lines=3,
                    max_lines=3,
                )

                image_size = gr.Dropdown(
                    label="Image Size",
                    info="Select the size of the image to generate.",
                    choices=[
                        "square_hd",
                        "square",
                        "portrait_4_3",
                        "portrait_16_9",
                        "landscape_4_3",
                        "landscape_16_9",
                    ],
                    interactive=True,
                    value="square_hd",
                )
                num_images = gr.Slider(
                    label="Number of Images",
                    minimum=1,
                    maximum=4,
                    step=1,
                    value=1,
                    interactive=True,
                )

            with gr.Column():
                outputs = gr.Gallery(label="Generated Image", show_label=True)
                generateButton: Dependency = gr.Button(value="Generate Image").click(
                    fn=subscribe,
                    inputs=[prompt, image_size, num_images],
                    outputs=[outputs],
                )

    return flux_interface
