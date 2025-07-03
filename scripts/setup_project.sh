#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to print colored output
print_color() {
    case "$1" in
        "green") echo -e "\033[0;32m$2\033[0m" ;;
        "yellow") echo -e "\033[0;33m$2\033[0m" ;;
        "red") echo -e "\033[0;31m$2\033[0m" ;;
    esac
}

# Initialize pyenv if it exists
if command -v pyenv &> /dev/null; then
    print_color "green" "Initializing pyenv..."
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# Navigate to the monorepo root
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR/.."

# Function to set up a project
setup_project() {
    local project_path=$1
    print_color "green" "\nSetting up project: $project_path"
    cd "$project_path"

    if [ ! -f "requirements.txt" ]; then
        print_color "yellow" "No requirements.txt found. Skipping."
        cd -
        return
    fi

    if [ ! -d ".venv" ]; then
        print_color "yellow" "Creating virtual environment..."
        python3 -m venv .venv
    fi

    print_color "green" "Activating virtual environment and installing dependencies..."
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    cd -
}

# Setup apps
for app_dir in apps/*; do
    if [ -d "$app_dir" ]; then
        setup_project "$app_dir"
    fi
done

# Setup libs
for lib_dir in libs/*; do
    if [ -d "$lib_dir" ]; then
        setup_project "$lib_dir"
    fi
done

print_color "green" "\nAll projects set up successfully!"