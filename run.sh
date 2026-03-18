#!/bin/bash
# Run script for BRNA Project

echo "======================================"
echo "    Starting BRNA Project"
echo "======================================"

# Determine base paths
BASE_DIR="$(pwd)"
CORE_DIR="$BASE_DIR/Github_artifact/pro10-brna-v2"
PORTAL_DIR="$BASE_DIR/brna-portal"

# Check if .venv exists
if [ ! -d "$CORE_DIR/.venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run ./setup.sh first to install requirements."
    exit 1
fi

echo ">>> Starting BRNA Backend API (FastAPI) on port 8000..."
cd "$PORTAL_DIR"
# Run FastAPI using the Core Engine's virtual environment python
"$CORE_DIR/.venv/bin/python3" main.py &
BACKEND_PID=$!

echo ">>> Starting BRNA Frontend Portal (Next.js) on port 3000..."
# Run Next.js normally
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "    Services are now running!"
echo "    Frontend: http://localhost:3000"
echo "    Backend:  http://localhost:8000"
echo "======================================"
echo "Press [CTRL+C] to stop all services."

# Trap CTRL+C and kill background processes
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
