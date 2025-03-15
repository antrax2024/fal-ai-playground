FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the application files
COPY main.py .
COPY pyproject.toml .
COPY modules modules
COPY assets assets


# Create virtual environment
RUN uv venv
# Install dependencies
RUN uv sync

# Expose the port the app runs on
EXPOSE 3206

# Command to run the application
CMD ["uv", "run","main.py"]