import gradio as gr
from modules.inpainting import create_inpainting_interface
from modules.flux import create_flux_interface

# Create interfaces for each tab
inpainting_interface: gr.Blocks = create_inpainting_interface()
flux_interface: gr.Blocks = create_flux_interface()

# Create tabbed interface (global scope)
demo = gr.TabbedInterface(
    interface_list=[inpainting_interface, flux_interface],
    tab_names=["Inpainting", "Flux"],
    title=":: FAL-AI Playground ::",
    theme="d8ahazard/rd_blue",
)


def main() -> None:
    # Launch the app
    demo.launch()


if __name__ == "__main__":
    main()
