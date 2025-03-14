import gradio as gr
from modules.inpainting import create_inpainting_interface
from modules.flux import create_flux_interface


def main():
    # Create interfaces for each tab
    inpainting_interface = create_inpainting_interface()
    flux_interface = create_flux_interface()

    # Create tabbed interface
    demo = gr.TabbedInterface(
        [inpainting_interface, flux_interface],
        ["Inpainting", "Flux"],
        title="FAL-AI Playground",
    )

    # Launch the app
    demo.launch()


if __name__ == "__main__":
    main()
