FROM python:3.10-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    zsh \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up Oh My Zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Set zsh as default shell for the container
RUN chsh -s /bin/zsh

# Set the working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000
