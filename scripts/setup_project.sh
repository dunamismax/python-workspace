#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Initialize pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Navigate to the monorepo root
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR/.."

# Function to set up a project
setup_project() {
    local project_path=$1
    echo "\nSetting up project: $project_path"
    cd "$project_path"

    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi

    echo "Activating virtual environment and installing dependencies..."
    source .venv/bin/activate
    pip install -r requirements.txt
    deactivate
    cd -
}

# Setup apps
for app_dir in apps/*;
do
    if [ -d "$app_dir" ]; then
        setup_project "$app_dir"
    fi
done

# Setup libs
for lib_dir in libs/*;
do
    if [ -d "$lib_dir" ]; then
        setup_project "$lib_dir"
    fi
done

echo "\nAll projects set up successfully!"

