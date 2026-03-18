#!/bin/bash

# BRNA - Bio-Resonance Network Architecture
# Simulation Setup & Execution Script

# Change to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "============================================================"
echo " BRNA Simulation: Bio-Resonance Network Architecture"
echo "============================================================"

# Check if .venv exists, if not create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/Update dependencies
echo "Verifying dependencies..."
pip install -q -r requirements.txt

# Run everything
if [ "$1" == "--test" ]; then
    echo "Running unit tests..."
    python3 -m pytest tests/
elif [ "$1" == "--dashboard" ]; then
    echo "Launching Live Dashboard (30s)..."
    python3 pro04-resonance-protocol/dashboard.py
else
    echo "Running Full Stack Simulation (Weeks 1-4)..."
    python3 run_simulation.py
    echo ""
    echo "To run tests: ./start.sh --test"
    echo "To run dashboard: ./start.sh --dashboard"
fi
