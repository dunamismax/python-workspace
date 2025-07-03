#!/bin/bash

# ==============================================================================
#
# Title:           Setup Python Environment with pyenv on macOS
# Description:     This script automates the following steps:
#                  1. Checks for and installs Homebrew.
#                  2. Installs pyenv and its build dependencies.
#                  3. Configures the user's .zshrc profile for pyenv.
#                  4. Installs a specified version of Python (3.12.8).
#                  5. Sets the installed version as the global default.
#
# Usage:           Save the script as setup_python_env.sh, give it
#                  execute permissions (chmod +x setup_python_env.sh),
#                  and run it (./setup_python_env.sh).
#
# Author:          Gemini
# Version:         1.0
#
# ==============================================================================

# --- Configuration ---
# Set the desired Python version here.
PYTHON_VERSION="3.12.8"
# Set the shell profile file. Modern macOS uses .zshrc.
PROFILE_FILE="$HOME/.zshrc"

# --- Helper Functions for Colored Output ---
Color_Off='\033[0m'
BRed='\033[1;31m'
BGreen='\033[1;32m'
BYellow='\033[1;33m'
BBlue='\033[1;34m'
BPurple='\033[1;35m'

log_info() {
  echo -e "${BBlue}INFO:${Color_Off} $1"
}

log_success() {
  echo -e "${BGreen}SUCCESS:${Color_Off} $1"
}

log_warn() {
  echo -e "${BYellow}WARNING:${Color_Off} $1"
}

log_error() {
  echo -e "${BRed}ERROR:${Color_Off} $1" >&2
}

# --- Main Script ---

log_info "Starting Python environment setup for version ${BPurple}${PYTHON_VERSION}${Color_Off}..."

# STEP 1: Check for and install Homebrew
if ! command -v brew &> /dev/null; then
  log_info "Homebrew not found. Installing now..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ $? -ne 0 ]]; then
    log_error "Homebrew installation failed. Please install it manually and run this script again."
    exit 1
  fi
  log_success "Homebrew installed successfully."
else
  log_info "Homebrew is already installed. Updating..."
  brew update
fi

# STEP 2: Install pyenv and its build dependencies
log_info "Installing pyenv and required Python build dependencies..."
# Dependencies like openssl and readline are recommended for building Python from source. [6]
brew install pyenv openssl readline sqlite3 xz zlib
log_success "pyenv and dependencies installed via Homebrew."

# STEP 3: Configure shell environment for pyenv
log_info "Configuring your shell profile at ${BPurple}${PROFILE_FILE}${Color_Off}..."

# Add pyenv to the shell profile if it's not already there.
# This ensures that pyenv's shims are in your PATH. [7]
if ! grep -q 'eval "$(pyenv init -)"' "$PROFILE_FILE"; then
  log_info "Adding pyenv configuration to ${PROFILE_FILE}..."
  echo '' >> "$PROFILE_FILE"
  echo '# --- pyenv configuration ---' >> "$PROFILE_FILE"
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$PROFILE_FILE"
  echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> "$PROFILE_FILE"
  echo 'eval "$(pyenv init -)"' >> "$PROFILE_FILE"
  log_success "pyenv configuration added."
else
  log_warn "pyenv configuration already exists in ${PROFILE_FILE}. Skipping."
fi

# Apply the new configuration to the current shell
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# STEP 4: Install the specified Python version
log_info "Installing Python ${PYTHON_VERSION} with pyenv..."
log_warn "This process can take several minutes as it compiles Python from source."

# Check if the version is already installed
if pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
  log_warn "Python version ${PYTHON_VERSION} is already installed. Skipping installation."
else
  pyenv install "$PYTHON_VERSION"
  if [[ $? -ne 0 ]]; then
    log_error "Failed to install Python ${PYTHON_VERSION}. Please check for build errors."
    exit 1
  fi
  log_success "Successfully installed Python ${PYTHON_VERSION}."
fi

# STEP 5: Set the global Python version
log_info "Setting global Python version to ${PYTHON_VERSION}..."
pyenv global "$PYTHON_VERSION"
log_success "Global Python version set."

# --- Final Instructions ---
echo
log_success "All steps completed!"
echo
echo -e "${BYellow}IMPORTANT:${Color_Off} For the changes to take full effect, you must ${BPurple}restart your terminal${Color_Off}."
echo "After restarting, you can verify the installation by running the following commands:"
echo
echo "  ${BGreen}pyenv versions${Color_Off}      (should show ${PYTHON_VERSION} with a * next to it)"
echo "  ${BGreen}which python${Color_Off}         (should point to the pyenv shims directory)"
echo "  ${BGreen}python --version${Color_Off}     (should output Python ${PYTHON_VERSION})"
echo