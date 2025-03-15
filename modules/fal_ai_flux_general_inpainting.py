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


def inpaintImage(inputImage, inputPrompt, numInferenceSteps, guidanceScale):
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
        "fal-ai/flux-general/inpainting",
        arguments={
            "prompt": f"{inputPrompt}",
            "num_inference_steps": numInferenceSteps,
            "controlnets": [],
            "controlnet_unions": [],
            "ip_adapters": [],
            "guidance_scale": guidanceScale,
            "real_cfg_scale": 3.5,
            "num_images": 1,
            "enable_safety_checker": False,
            "reference_strength": 0.65,
            "reference_end": 1,
            "base_shift": 0.5,
            "max_shift": 1.15,
            "image_url": f"{sourceURL}",
            "strength": 0.85,
            "mask_url": f"{maskURL}",
            "image_size": None,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    # print(result)
    # print(result["images"][0]["url"])
    # delete images
    os.remove("sourceImage.png")
    os.remove("maskImage.png")
    return result["images"][0]["url"]


def createFalAiFluxGeneralInpainting() -> gr.Blocks:
    """Creates and returns the flux interface"""
    with gr.Blocks() as fluxGeneralInpaintingInterface:
        gr.Markdown(value="# fal-ai/flux-general/inpainting")
        gr.Markdown(
            value="FLUX General Inpainting is a versatile endpoint that enables precise image editing and completion, supporting multiple AI extensions including LoRA, ControlNet, and IP-Adapter."
        )

        with gr.Row():
            inputPrompt = gr.Textbox(
                label="Prompt",
                placeholder="Describe the animation you want to create...",
                lines=3,
                max_lines=3,
            )
        with gr.Row():

            inputImage = gr.ImageMask(
                type="pil",
                label="Input Image",
            )

        with gr.Row():
            numInferenceSteps = gr.Slider(
                label="Number of Inference Steps",
                minimum=1,
                maximum=50,
                interactive=True,
                step=1,
                value=28,
            )
        with gr.Row():
            guidanceScale = gr.Slider(
                label="Guidance Scale",
                minimum=0,
                maximum=20,
                interactive=True,
                step=0.5,
                value=5,
            )
        with gr.Row():
            # Gallery to display the generated images
            outputImage = gr.Image(
                type="filepath", label="Output Image", interactive=False
            )
        with gr.Row():
            # button to generate the image
            generateButton: Dependency = gr.Button(value="Generate Image").click(
                fn=inpaintImage,
                inputs=[inputImage, inputPrompt, numInferenceSteps, guidanceScale],
                outputs=[outputImage],
            )

    return fluxGeneralInpaintingInterface
