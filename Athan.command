#!/bin/bash
cd "$(dirname "$0")"

# Find a Python 3.10+ (system Python 3.9 has broken tkinter on modern macOS)
PYTHON=""
for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 python3; do
    if command -v "$candidate" &> /dev/null; then
        ver=$("$candidate" -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
        if [ -n "$ver" ] && [ "$ver" -ge 10 ] 2>/dev/null; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo ""
    echo "  Python 3.10 or newer is required."
    echo "  Your Mac has Python 3.9 which has a broken UI library."
    echo ""
    echo "  Install Python with:  brew install python3"
    echo "  Or download from:     https://www.python.org/downloads/"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Create venv and install dependencies (only on first run)
if [ ! -d "venv" ]; then
    echo "First run — setting up..."
    "$PYTHON" -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Launch the app
python main.py
