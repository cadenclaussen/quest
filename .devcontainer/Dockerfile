# Base image: Microsoft's official Python 3.11 dev container on Debian Bullseye
# Includes Python, pip, and common dev container utilities
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install system packages needed for development
# DEBIAN_FRONTEND=noninteractive prevents prompts during installation
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        curl \
        wget \
        git \
        vim \
        nano \
        htop \
        tree \
        jq \
        zip \
        unzip \
        build-essential \
        ca-certificates \
        gnupg \
        lsb-release \
        software-properties-common

# Note: Claude Code CLI installation skipped (install manually if needed)

# Upgrade Python package management tools to latest versions
RUN pip install --upgrade pip setuptools wheel

# Install essential Python development packages
RUN pip install \
    poetry \
    pipenv \
    black \
    flake8 \
    isort \
    mypy \
    pytest \
    pytest-cov \
    ipython \
    rich \
    typer \
    click \
    pydantic \
    httpx \
    aiohttp \
    python-dotenv

# Create and set working directory
# This is where your project files will be mounted
RUN mkdir -p /workspace
WORKDIR /workspace

# Ensure the vscode user (non-root) owns the workspace directory
# Important for security - running as non-root user
RUN chown -R vscode:vscode /workspace