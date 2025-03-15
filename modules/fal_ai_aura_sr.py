from typing import Any, Dict
import gradio as gr
import fal_client
from rich.console import Console
from modules.common import uploadFile

cl = Console()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            cl.print(log["message"])


async def subscribe(inputImage) -> list[Any]:
    cl.print("[bold green]\n\n==============================================")
    cl.print("[bold green]Subscribing...")
    cl.print(f"[bold green]image_url: [yellow]{inputImage}[/yellow]")
    cl.print("[bold green]==============================================\n\n")
    imageURL: str = uploadFile(filePath=inputImage)
    cl.print(f"imageURL: {imageURL}")
    result = fal_client.subscribe(
        "fal-ai/aura-sr",
        arguments={
            "image_url": f"{imageURL}",
            "upscaling_factor": 4,
            "overlapping_tiles": True,
            "checkpoint": "v2",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    cl.print(f"Result: {result}")

    return result["image"]["url"]


def createFalAiAuraSr() -> gr.Blocks:
    with gr.Blocks() as auraSrInterface:
        gr.Markdown(value="# fal-ai/aura-sr")
        gr.Markdown(value="Upscale your images with AuraSR.")

        with gr.Row():
            with gr.Column():
                inputImage = gr.Image(
                    label="Input Image",
                    type="filepath",
                )

            with gr.Column():
                # Gallery to display the generated images
                outputImage = gr.Image(label="Output Image", interactive=False)
                # button to generate the image
                generateButton = gr.Button(value="Generate Image").click(
                    fn=subscribe,
                    inputs=[inputImage],
                    outputs=[outputImage],
                )

    return auraSrInterface
