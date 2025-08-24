# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quest is an AI development environment focused on Python and LangChain applications. The project is structured as a simple Python package with demonstration code for LangChain integration using Anthropic's Claude.

## Development Commands

### Core Development
- `npm run dev` - Run the main LangChain demo (src/main.py)
- `npm run clean` - Remove Python cache files and __pycache__ directories

### Notifications
- Commands for sending notifications via Claude CLI
- Configuration stored in `.claude/commands/notify.yaml`

## Code Architecture

### Structure  
- `/src/` - Main Python source code
  - `main.py` - Simple LangChain hello world demonstrating 4 key steps
- `/.claude/` - Claude CLI configuration and commands
  - `commands/` - Custom Claude commands including notification system
- `/.github/` - GitHub Actions workflows for CI/CD

### Key Components
- **LangChain Integration**: The project demonstrates basic LangChain usage with Anthropic's Claude including LLM initialization, prompt templates, and chain creation
- **Environment Configuration**: Uses python-dotenv for environment variable management (requires ANTHROPIC_API_KEY)
- **Claude CLI Integration**: Custom commands and notifications system

## Environment Requirements
- Python >= 3.9.0
- Node.js >= 18.0.0
- Anthropic API key required for LangChain functionality

## GitHub Actions
- Automated CI/CD workflows
- Security scanning
- Issue management and labeling
- Release automation