FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI (ARM64 version)
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# Copy requirements first for better caching
COPY package.json ./
RUN if [ -f "package.json" ]; then \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs; \
    fi

# Copy Python requirements if they exist
COPY requirements.txt* ./
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# Copy source code
COPY src/ ./src/
COPY . .

# Environment variables for AWS (will be provided at runtime)
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_DEFAULT_REGION=""
ENV ANTHROPIC_API_KEY=""

# Expose port for Streamlit
EXPOSE 8501

# Default command
CMD ["python", "src/hello_langchain.py"]