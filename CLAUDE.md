# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quest is an AI development environment focused on Python, LangChain, and LangGraph applications. The project is structured as a simple Python package with demonstration code for LangChain integration.

## Development Commands

### Core Development
- `npm run dev` - Start Streamlit app on port 8501
- `npm run jupyter` - Launch Jupyter Lab on port 8888
- `npm run test` - Run pytest with coverage reporting
- `npm run lint` - Format and lint code (black, isort, flake8)
- `npm run format` - Format code only (black, isort)
- `npm run clean` - Remove Python cache files and __pycache__ directories
- `npm run security` - Run security checks with safety and bandit

### Docker Development
- `npm run docker:build` - Build development container
- `npm run docker:run` - Run container with workspace mounted
- ECR deployment commands available for AWS integration

## Code Architecture

### Structure
- `/src/` - Main Python source code
  - `hello_langchain.py` - Main entry point and LangChain demonstration
  - `__init__.py` - Package initialization

### Key Components
- **LangChain Integration**: The project demonstrates basic LangChain usage including LLM initialization, prompt templates, and chain creation
- **Environment Configuration**: Uses python-dotenv for environment variable management (requires ANTHROPIC_API_KEY)
- **Streamlit Integration**: Primary web interface framework (app.py referenced but not yet created)

## Environment Requirements
- Python >= 3.9.0
- Node.js >= 18.0.0
- Anthropic API key required for LangChain functionality

## Testing and Quality
- pytest for testing with coverage reporting
- black and isort for code formatting
- flake8 for linting
- bandit and safety for security scanning