#!/bin/bash
# Setup script for BRNA Project

echo "======================================"
echo "    BRNA Project Setup Script"
echo "======================================"

echo ""
echo "[1/2] Setting up Python Environment for Core Engine & Backend..."
cd Github_artifact/pro10-brna-v2
# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created new virtual environment in .venv"
fi

# Activate and install requirements
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ../../
echo "Python environment setup complete."

echo ""
echo "[2/2] Setting up Node Environment for Frontend Portal..."
cd brna-portal
npm install
cd ..
echo "Node environment setup complete."

echo ""
echo "======================================"
echo " Setup Completed Successfully!"
echo "======================================"
echo "You can now run the project by executing: ./run.sh"
echo "Or manually follow the steps in README.md"
