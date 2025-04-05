#!/bin/bash

# Install Python using brew if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python using brew..."
    brew install python
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages using pip within the virtual environment
echo "Installing required packages..."
pip install openai python-dotenv langchain langchain-openai

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    echo "Please edit .env file and add your OpenAI API key"
fi

echo "Setup complete! To start using the analyzer:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the test script: python test_analyzer.py" 