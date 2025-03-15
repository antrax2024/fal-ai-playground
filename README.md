# FAL.ai Playground

This repository is a playground for experimenting with [FAL.ai](https://fal.ai), a platform for deploying and running AI models at scale. Use this space to test various AI models, build applications, and explore the capabilities of FAL.ai.

## Getting Started

### Prerequisites

- **uv** the extremely fast Python package and project manager, written in Rust.
- Python 3.12>=
- FAL.ai account and API key

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/fal-ai-playground.git
    cd fal-ai-playground
    ```

2. Set up your environment:

    ```bash
    # Create and activate virtual environment
    uv venv --python 3.12
    source venv/bin/activate
    
    # Install dependencies
    uv sync
    ```

3. Configure your FAL.ai credentials:

    ```bash
    # if you using bash
    export FAL_KEY="your-api-key"
    # if you use fish shell
    set -gx FAL_KEY "your-api-key"
    ```

4. Run the project

    ```bash
    uv run gradio main.py
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FAL.ai](https://fal.ai) for providing the platform
- Contributors and maintainers of this project
