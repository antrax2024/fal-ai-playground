from typing import Any, Dict
import gradio as gr
import fal_client
from rich.console import Console

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


def createFalAiAuraSr() -> gr.Blocks:
    with gr.Blocks() as auraSrInterface:
        gr.Markdown(value="# fal-ai/aura-sr")
        gr.Markdown(value="Upscale your images with AuraSR.")

        with gr.Row():
            with gr.Column():
                inputImage = gr.Image(
                    label="Input Image",
                )

            with gr.Column():
                # Gallery to display the generated images
                outputImage = gr.Image(label="Output Image", interactive=False)
                # button to generate the image
                # generateButton: Dependency = gr.Button(value="Generate Image").click(
                #     fn=subscribe,
                #     inputs=[prompt, image_size, num_images],
                #     outputs=[outputs],
                # )

    return auraSrInterface
