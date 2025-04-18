FROM python:3.14.0a7-alpine3.21

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the timezone
ENV TZ=America/Sao_Paulo

# User Name
ARG USER_NAME=appuser
# Group Name
ARG GROUP_NAME=appgroup

# add non-root user
RUN addgroup -S ${GROUP_NAME} && adduser -S ${USER_NAME} -G ${GROUP_NAME}

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app
RUN chown -R ${USER_NAME}:${GROUP_NAME} /app

# Set the user to the non-root user
USER ${USER_NAME}

# Create virtual environment
RUN uv venv --python 3.13 .venv

# Expose the port the app runs on
EXPOSE 3206

# Command to run the application
CMD uv run main.py