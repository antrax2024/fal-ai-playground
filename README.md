
# fal.ai Playground

This repository is a playground for experimenting with [fal.ai](https://fal.ai), a platform for deploying and running AI models at scale. Use this space to test various AI models, build applications, and explore the capabilities of fal.ai.

## Screenshot

![Application Screenshot](/assets/screenshot.jpg)

## Getting Started

### Prerequisites

- **uv** the extremely fast Python package and project manager, written in Rust.
- Python 3.12
- fal.ai account and API key

### Installation

#### Clone this repository

```bash
git clone https://github.com/antrax2024/fal-ai-playground.git
cd fal-ai-playground
```

#### Set up your environment

```bash
# Create and activate virtual environment
uv venv --python 3.13
source venv/bin/activate

# Install dependencies
uv sync
```

#### Configure your fal.ai credentials

```bash
# if you using bash
export FAL_KEY="your-api-key"
# if you use fish shell
set -gx FAL_KEY "your-api-key"
```

#### Run the project

```bash
uv run gradio main.py
```

### Running with docker

Verify ports if your host 3206 ports is free. If no, edit the Dockerfile and docker-build to mapping to correct port.
Edit **docker-compose.yml** and change parameters if necessary. 

```bash
./build.sh
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FAL.ai](https://fal.ai) for providing the platform
- Contributors and maintainers of this project
