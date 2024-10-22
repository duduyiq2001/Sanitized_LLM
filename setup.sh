#!/bin/bash

# Update and install system dependencies
echo "Updating system and installing essential packages..."
sudo apt-get update
sudo apt-get install -y python3-pip 


# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install necessary Python dependencies
echo "Installing Python dependencies..."
pip install transformers
pip install torch  # Assuming you'll use PyTorch on the H100
pip install sentencepiece  # Needed for LLaMA models
pip install pandas  # If you're working with CSVs
pip install accelerate  # For multi-GPU support and optimization
pip install -U sentence-transformers
pip install tf-keras

# Optional: Install any other libraries you might need based on your project
# For example, if you need extra libraries, you can add them here

# Confirm installations
echo "Confirming installed packages..."
pip freeze

echo "All dependencies are installed, and the environment is set up."
