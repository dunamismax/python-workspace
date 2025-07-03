#!/bin/bash

# Navigate to the monorepo root
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR"

# Activate the cli_launcher's virtual environment
source apps/cli_launcher/.venv/bin/activate

# Run the cli_launcher
python -m apps.cli_launcher.src.cli_launcher.main

# Deactivate the virtual environment (optional, but good practice)
deactivate
