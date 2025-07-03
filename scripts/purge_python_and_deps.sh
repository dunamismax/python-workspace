#!/bin/bash

# ==============================================================================
#
# Title:           Purge Homebrew Python and Dependent Packages
# Description:     This script completely uninstalls all Homebrew Python versions
#                  and a specified list of packages that depend on them.
#
#                  The script will:
#                  1. Find all Homebrew packages starting with 'python'.
#                  2. Add 'git-filter-repo', 'meson', 'pipx', 'uvicorn',
#                     and 'yt-dlp' to the list.
#                  3. Display a final list of ALL packages to be removed.
#                  4. Ask for explicit user confirmation before proceeding.
#                  5. Uninstall all listed packages.
#
# Usage:           Save as purge_python_and_deps.sh, make it executable
#                  (chmod +x purge_python_and_deps.sh), and run it
#                  (./purge_python_and_deps.sh).
#
# ==============================================================================

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

# --- Configuration ---
# List of specific packages to remove in addition to Python versions.
EXPLICIT_PACKAGES="git-filter-repo meson pipx uvicorn yt-dlp"

# --- Main Script ---

log_info "Starting cleanup of Python and its dependent packages."
echo

# STEP 1: Find all Homebrew-installed python packages
log_info "Searching for Homebrew packages starting with 'python'..."
PYTHON_PACKAGES=$(brew list --formula | grep '^python')

# STEP 2: Combine the lists of packages to be removed
# We combine the dynamically found Python packages with the explicit list.
# 'tr' puts each package on a new line, 'sort -u' removes duplicates,
# and the final 'tr' puts them back on one line for the command.
ALL_PACKAGES_TO_UNINSTALL=$(echo "$PYTHON_PACKAGES $EXPLICIT_PACKAGES" | tr ' ' '\n' | sort -u | tr '\n' ' ')

if [ -z "$ALL_PACKAGES_TO_UNINSTALL" ]; then
  log_success "No relevant packages were found to uninstall. Your system is clean. Exiting."
  exit 0
fi

# STEP 3: Display warnings and the final list of packages
log_warn "---------------------- ATTENTION ----------------------"
log_warn "This script will permanently uninstall the following packages"
log_warn "from your system. This action cannot be undone."
log_warn "---------------------------------------------------------"
echo

log_info "The following packages have been targeted for complete removal:"
echo -e "${BPurple}${ALL_PACKAGES_TO_UNINSTALL}${Color_Off}"
echo

# STEP 4: Ask for final confirmation
log_warn "Are you absolutely sure you want to uninstall all packages listed above?"
echo -n -e "${BYellow}This action is permanent. (y/n): ${Color_Off}"
read -r response

if [[ "$response" != "y" ]]; then
  log_info "Operation cancelled by user. Your system has not been modified."
  exit 0
fi

# STEP 5: Execute the uninstallation
log_info "User confirmed. Proceeding with uninstallation..."

# The 'brew uninstall' command can take multiple package names at once.
# By removing the dependents and dependencies together, we avoid errors.
brew uninstall $ALL_PACKAGES_TO_UNINSTALL

if [[ $? -eq 0 ]]; then
  log_success "All specified packages have been successfully uninstalled."
else
  log_error "An error occurred during uninstallation. Please check the output from Homebrew."
fi

# Optional: Suggest running brew autoremove to clean up any other orphaned dependencies.
log_info "You may want to run 'brew autoremove' to clean up any other unused dependencies."
echo
log_info "Script finished."