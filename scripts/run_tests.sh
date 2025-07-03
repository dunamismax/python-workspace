#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to run tests for a project
run_tests() {
    local project_path=$1
    echo "\nRunning tests for project: $project_path"
    cd "$project_path"

    if [ -d ".venv" ]; then
        source .venv/bin/activate
        pytest
        deactivate
    else
        echo "No virtual environment found. Please run setup_project.sh first."
    fi
    cd -
}

# Run tests for apps
for app_dir in apps/*;
do
    if [ -d "$app_dir" ]; then
        run_tests "$app_dir"
    fi
done

# Run tests for libs
for lib_dir in libs/*;
do
    if [ -d "$lib_dir" ]; then
        run_tests "$lib_dir"
    fi
done

echo "\nAll tests completed!"

