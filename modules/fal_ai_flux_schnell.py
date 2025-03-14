from typing import Any, Dict
import gradio as gr
import fal_client
from rich.console import Console


from gradio.events import Dependency

cl = Console()


async def subscribe(prompt, image_size, num_images) -> list[Any]:
    cl.print("[bold green]\n\n==============================================")
    cl.print("[bold green]Subscribing...")
    cl.print(f"[bold green]Prompt: [white]{prompt}")
    cl.print(f"[bold green]Image Size:[white] {image_size}")
    cl.print(f"[bold green]Number of Images: [white]{num_images}")
    cl.print("[bold green]==============================================\n\n")
    handler: fal_client.AsyncRequestHandle = await fal_client.submit_async(
        application="fal-ai/flux/schnell",
        arguments={
            "prompt": f"{prompt}",
            "image_size": f"{image_size}",
            "num_inference_steps": 4,
            "num_images": num_images,
            "enable_safety_checker": False,
            "with_logs": True,
        },
    )

    request_id: str = handler.request_id
    cl.print(f"Request ID: {request_id}")

    async for event in handler.iter_events(with_logs=True):
        print(event)

    result: Dict[str, Any] = await handler.get()
    cl.print(f"Result: {result}")

    # Extract only the URLs from the images array
    image_urls: list[Any] = [image["url"] for image in result["images"]]
    cl.print(f"Image URLs: {image_urls}\n\n\n")
    return image_urls


def fal_ai_flux_schnell_interface() -> gr.Blocks:
    """Creates and returns the flux interface"""
    with gr.Blocks() as flux_schnell_interface:
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
                # Gallery to display the generated images
                outputs = gr.Gallery(label="Generated Image", show_label=True)
                # button to generate the image
                generateButton: Dependency = gr.Button(value="Generate Image").click(
                    fn=subscribe,
                    inputs=[prompt, image_size, num_images],
                    outputs=[outputs],
                )

    return flux_schnell_interface
