from typing import Any, Dict
import gradio as gr
import fal_client
from rich.console import Console
from gradio.events import Dependency

cl = Console()


async def subscribe(prompt, aspect_ratio, num_images) -> list[Any]:
    cl.print("[bold green]\n\n==============================================")
    cl.print("[bold green]Subscribing...")
    cl.print(f"[bold green]Prompt: [white]{prompt}")
    cl.print(f"[bold green]Number of Images: [white]{num_images}")
    cl.print(f"[bold green]Aspect Ratio: [white]{aspect_ratio}")
    cl.print("[bold green]==============================================\n\n")
    handler: fal_client.AsyncRequestHandle = await fal_client.submit_async(
        application="fal-ai/flux-pro/v1.1-ultra",
        arguments={
            "prompt": f"{prompt}",
            "aspect_ratio": f"{aspect_ratio}",
            "num_images": num_images,
            "enable_safety_checker": False,
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


def createFalAiProV11Ultra() -> gr.Blocks:
    """Creates and returns the flux interface"""
    with gr.Blocks() as fluxProV11UltraInterface:
        gr.Markdown(value="# fal-ai/flux-pro/v1.1-ultra")
        gr.Markdown(
            value="FLUX1.1 [pro] ultra is the newest version of FLUX1.1 [pro], maintaining professional-grade image quality while delivering up to 2K resolution with improved photo realism."
        )

        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe the animation you want to create...",
                    lines=3,
                    max_lines=3,
                )

                aspect_ratio = gr.Dropdown(
                    label="Aspect Ratio",
                    info="The aspect ratio of the generated image.",
                    choices=[
                        "21:9",
                        "16:9",
                        "4:3",
                        "3:2",
                        "1:1",
                        "2:3",
                        "3:4",
                        "9:16",
                        "9:21",
                    ],
                    interactive=True,
                    value="4:3",
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
                    inputs=[prompt, aspect_ratio, num_images],
                    outputs=[outputs],
                )

    return fluxProV11UltraInterface
