import gradio as gr
import base64
from gradio.components import image
from modules.inpainting import create_inpainting_interface
from modules.fal_ai_flux_schnell import create_flux_interface
import os

# Create interfaces for each tab
inpainting_interface: gr.Blocks = create_inpainting_interface()
flux_interface: gr.Blocks = create_flux_interface()

# Get the current directory (full path)
current_directory: str = os.path.dirname(os.path.abspath(path=__file__))
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
        <span
            style='font-size: 1.5em; font-weight: bold;'
        >
            FAL-AI Playground
        </span>
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
        interface_list=[inpainting_interface, flux_interface],
        tab_names=["Inpainting", "Flux"],
    )


def main() -> None:
    # Launch the app
    demo.launch(
        debug=True,
        server_port=3205,
        server_name="0.0.0.0",
    )


if __name__ == "__main__":
    main()
