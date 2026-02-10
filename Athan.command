#!/bin/bash
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required. Install it from https://www.python.org/downloads/"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Create venv and install dependencies (only on first run)
if [ ! -d "venv" ]; then
    echo "First run — setting up..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Launch the app
python main.py
