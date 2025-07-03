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

# Navigate to the monorepo root
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR/.."

# Function to run tests for a project
run_tests() {
    local project_path=$1
    print_color "green" "\nRunning tests for project: $project_path"
    cd "$project_path"

    if [ ! -d ".venv" ]; then
        print_color "yellow" "No virtual environment found. Skipping."
        cd -
        return
    fi

    source .venv/bin/activate
    if ! command -v pytest &> /dev/null; then
        print_color "yellow" "pytest not found. Installing..."
        pip install pytest
    fi
    
    if [ -d "tests" ]; then
        pytest
    else
        print_color "yellow" "No 'tests' directory found. Skipping."
    fi
    
    deactivate
    cd -
}

# Run tests for apps
for app_dir in apps/*; do
    if [ -d "$app_dir" ]; then
        run_tests "$app_dir"
    fi
done

# Run tests for libs
for lib_dir in libs/*; do
    if [ -d "$lib_dir" ]; then
        run_tests "$lib_dir"
    fi
done

print_color "green" "\nAll tests completed!"