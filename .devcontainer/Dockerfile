# Base image: Microsoft's official Python 3.11 dev container on Debian Bullseye
# Includes Python, pip, and common dev container utilities
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install system packages needed for development
# DEBIAN_FRONTEND=noninteractive prevents prompts during installation
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        curl \                    # HTTP client for downloading files
        wget \                    # Alternative HTTP client
        git \                     # Version control (backup, features may override)
        vim \                     # Terminal text editor
        nano \                    # Simpler terminal text editor
        htop \                    # Interactive process viewer
        tree \                    # Directory structure viewer
        jq \                      # JSON processor for CLI
        zip \                     # Archive creation
        unzip \                   # Archive extraction
        build-essential \         # C/C++ compiler and build tools
        ca-certificates \         # SSL certificates for HTTPS
        gnupg \                   # GNU Privacy Guard for security
        lsb-release \             # Linux Standard Base release info
        software-properties-common # Manage software repositories

# Install Claude Code CLI - your AI coding assistant
# Downloads and runs the official installer script
RUN curl -fsSL https://claude.ai/install.sh | sh

# Upgrade Python package management tools to latest versions
RUN pip install --upgrade pip setuptools wheel

# Install essential Python development packages
RUN pip install \
    poetry \              # Modern dependency management
    pipenv \              # Alternative dependency management
    black \               # Code formatter (opinionated)
    flake8 \              # Linting for code quality
    isort \               # Import statement organizer
    mypy \                # Static type checker
    pytest \             # Testing framework
    pytest-cov \         # Test coverage reports
    ipython \            # Enhanced interactive Python shell
    rich \               # Beautiful terminal output
    typer \              # CLI framework
    click \              # Alternative CLI framework
    pydantic \           # Data validation using type hints
    httpx \              # Modern HTTP client
    aiohttp \            # Async HTTP client/server
    python-dotenv        # Load environment variables from .env files

# Create and set working directory
# This is where your project files will be mounted
RUN mkdir -p /workspace
WORKDIR /workspace

# Ensure the vscode user (non-root) owns the workspace directory
# Important for security - running as non-root user
RUN chown -R vscode:vscode /workspace