import gradio as gr
import fal_client
from rich.console import Console
import os


from gradio.events import Dependency

cl = Console()


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            cl.print(log["message"])


def fillImage(inputImage, inputPrompt, safety_tolerance):
    cl.print("Inpainting image")
    cl.print(f"Saving source image...")
    sourceImage = inputImage["background"]
    sourceImage.save("sourceImage.png")
    width, height = sourceImage.size
    cl.print(f"Source image size: {width}x{height}")

    cl.print(f"Saving the mask...")
    mask = inputImage["layers"][0]
    alpha_channel = mask.split()[3]
    maskImage = alpha_channel.point(lambda p: p > 0 and 255)
    maskImage.save("maskImage.png")

    cl.print("Uploading original image...")
    sourceURL = fal_client.upload_file("./sourceImage.png")
    cl.print(f"Uploaded sourceImage URL: {sourceURL}")

    cl.print("Uploading mask image...")
    maskURL = fal_client.upload_file("./maskImage.png")
    cl.print(f"Uploaded maskImage URL: {maskURL}")

    cl.print("Requesting to fal.ai...")

    result = fal_client.subscribe(
        "fal-ai/flux-pro/v1/fill",
        arguments={
            "prompt": f"{inputPrompt}",
            "num_images": 1,
            "safety_tolerance": f"{safety_tolerance}",
            "output_format": "jpeg",
            "image_url": f"{sourceURL}",
            "mask_url": f"{maskURL}",
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    cl.print(f"Result: {result}")

    os.remove(path="sourceImage.png")
    os.remove(path="maskImage.png")
    return result["images"][0]["url"]


def createFalAiFluxProV1Fill() -> gr.Blocks:
    with gr.Blocks() as FluxProV1FillInterface:
        gr.Markdown(value="# fal-ai/flux-pro/v1/fill")
        gr.Markdown(
            value="FLUX.1 [pro] Fill is a high-performance endpoint for the FLUX.1 [pro] model that enables rapid transformation of existing images, delivering high-quality style transfers and image modifications with the core FLUX capabilities."
        )

        with gr.Row():
            inputImage = gr.ImageMask(
                type="pil",
                label="Input Image",
            )

        with gr.Row():
            inputPrompt = gr.Textbox(
                label="Prompt",
                info="The prompt to fill the masked part of the image.",
                lines=2,
                max_lines=2,
            )

        with gr.Row():

            safety_tolerance = gr.Slider(
                label="Safety Tolerance",
                info="The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: 2",
                minimum=1,
                maximum=5,
                interactive=True,
                step=1,
                value=1,
            )
        with gr.Row():
            # Gallery to display the generated images
            outputImage = gr.Image(
                type="filepath", label="Output Image", interactive=False
            )
        with gr.Row():
            # button to generate the image
            generateButton: Dependency = gr.Button(value="Generate Image").click(
                fn=fillImage,
                inputs=[inputImage, inputPrompt, safety_tolerance],
                outputs=[outputImage],
            )

    return FluxProV1FillInterface
