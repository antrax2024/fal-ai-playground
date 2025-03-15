import gradio as gr
import base64
from modules.fal_ai_flux_pro_v1_1_ultra import createFalAiProV11Ultra
from modules.fal_ai_flux_schnell import createFalAiFluxSchnell
from modules.fal_ai_flux_general_inpainting import createFalAiFluxGeneralInpainting
import os

VERSION = "0.1.2"


# Create interfaces for each tab
flux_schnell_interface: gr.Blocks = createFalAiFluxSchnell()
flux_pro_v1_1_ultra_interface: gr.Blocks = createFalAiProV11Ultra()
fluxGeneralInpaintingInterface = createFalAiFluxGeneralInpainting()

# Get the current directory (full path)
current_directory: str = os.path.dirname(p=os.path.abspath(path=__file__))
# Get the path to the image file
image_path: str = os.path.join(current_directory, "assets", "logo.png")

# Ler a imagem e convertê-la para base64
with open(file=image_path, mode="rb") as image_file:
    encoded_string: str = base64.b64encode(s=image_file.read()).decode()


# Definindo o diretório de assets
# Definindo o diretório de assets
HEADER_HTML: str = f"""
    <div style='display: flex; align-items: center; justify-content: flex-start; padding: 10px; margin-top: -20px; padding-bottom: 0;'>
        <img 
            src='data:image/png;base64,{encoded_string}'
            style='width: 10%; margin-right: 20px;'
            alt='Logo'     
        >
        <div style='display: flex; flex-direction: column;'>
            <span
                style='font-size: 1.5em; font-weight: bold;'
            >
                fal.ai Playground
            </span>
            <span style='font-size: 0.8em;'>Version {VERSION}</span>
        </div>
    </div>
"""

# Create the header component
header = gr.HTML(value=HEADER_HTML)


# Criar a interface completa com Blocks
with gr.Blocks(theme="d8ahazard/rd_blue", title="fal.ai Playground") as demo:
    # Adicionar o header
    gr.HTML(value=HEADER_HTML)

    # Adicionar a interface com abas
    gr.TabbedInterface(
        interface_list=[
            flux_schnell_interface,
            flux_pro_v1_1_ultra_interface,
            fluxGeneralInpaintingInterface,
        ],
        tab_names=["flux/schnell", "flux/pro/v1_1/ultra", "flux-general/inpainting"],
    )


def main() -> None:
    # Launch the app
    demo.launch(
        debug=True,
        server_port=3206,
        server_name="0.0.0.0",
    )


if __name__ == "__main__":
    main()
