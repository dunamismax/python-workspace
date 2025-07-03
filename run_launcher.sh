#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the monorepo root
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR"

# Define the path to the cli_launcher's virtual environment
VENV_PATH="apps/cli_launcher/.venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "CLI Launcher virtual environment not found. Please run 'scripts/setup_project.sh' first."
    exit 1
fi

# Activate the cli_launcher's virtual environment
source "$VENV_PATH/bin/activate"

# Run the cli_launcher
python -m cli_launcher.main

# Deactivate the virtual environment
deactivate