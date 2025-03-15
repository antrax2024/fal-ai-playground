from typing import Any, Dict
import gradio as gr
import fal_client
from rich.console import Console
from modules.common import uploadFile


from gradio.events import Dependency

cl = Console()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            cl.print(log["message"])


def subscribe(
    inputPrompt, inputImage, strength, guidance_scale, num_images
) -> list[Any]:
    cl.print("[bold green]\n\n==============================================")
    cl.print("[bold green]Subscribing...")
    cl.print(f"[bold green]inputPrompt: [yellow]{inputPrompt}")
    cl.print(f"[bold green]inputImage: [yellow]{inputImage}")
    cl.print(f"[bold green]strength: [yellow]{strength}")
    cl.print(f"[bold green]guidance_scale: [yellow]{guidance_scale}")
    cl.print(f"[bold green]num_images: [yellow]{num_images}")
    cl.print("[bold green]==============================================\n\n")

    cl.print("[bold green]Uploading image...")
    image_url = uploadFile(inputImage)
    cl.print(f"[bold green]Image URL: [yellow]{image_url}")

    result = fal_client.subscribe(
        "fal-ai/flux/dev/image-to-image",
        arguments={
            "image_url": f"{image_url}",
            "prompt": f"{inputPrompt}",
            "strength": strength,
            "num_inference_steps": 40,
            "guidance_scale": guidance_scale,
            "num_images": num_images,
            "enable_safety_checker": True,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    cl.print(f"Result: {result}")

    # Extract only the URLs from the images array
    image_urls: list[Any] = [image["url"] for image in result["images"]]
    cl.print(f"Image URLs: {image_urls}\n\n\n")
    return image_urls


def createFluxDevImageToImage() -> gr.Blocks:
    with gr.Blocks() as fluxDevImageToImageInterface:
        gr.Markdown(value="# flux/dev/image-to-image")
        gr.Markdown(
            value="FLUX.1 [schnell] is a 12 billion parameter flow transformer that generates high-quality images from text in 1 to 4 steps, suitable for personal and commercial use."
        )

        with gr.Row():
            inputImage = gr.Image(
                label="Input Image",
                type="filepath",
            )
        with gr.Row():
            inputPrompt = gr.Textbox(label="Prompt", lines=2, max_lines=2)
            strength = gr.Slider(
                label="Strength",
                info="The strength of the initial image. Higher strength values are better for this model. Default value: 0.95",
                minimum=0.01,
                maximum=1.0,
                step=0.05,
                value=0.95,
                interactive=True,
            )

            guidance_scale = gr.Slider(
                label="Guidance Scale",
                info="The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5",
                minimum=1,
                maximum=20,
                step=0.5,
                value=3.5,
                interactive=True,
            )

            num_images = gr.Slider(
                label="Number of Images",
                info="The number of images to generate. Default value: 1",
                minimum=1,
                maximum=5,
                step=1,
                value=1,
                interactive=True,
            )

        with gr.Row():
            # Gallery to display the generated images
            outputs = gr.Gallery(label="Generated Image", show_label=True)
        with gr.Row():
            # button to generate the image
            generateButton: Dependency = gr.Button(value="Generate Image").click(
                fn=subscribe,
                inputs=[inputPrompt, inputImage, strength, guidance_scale, num_images],
                outputs=[outputs],
            )

    return fluxDevImageToImageInterface
