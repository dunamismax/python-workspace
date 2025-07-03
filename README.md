<p align="center">
  <img src="./python-workspace-image.png" alt="Python Monorepo logo" width="250"/>
</p>

Welcome to my Python Monorepo. This repository centralizes diverse Python applications and reusable libraries, designed for efficient, scalable, and maintainable project management across various domains like CLI tools, web services, and data processing.

[![Language: Python](https://img.shields.io/badge/Language-Python-3776AB.svg)](https://www.python.org/)
[![Web Framework: FastAPI](https://img.shields.io/badge/Web%20Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![CLI Framework: Rich](https://img.shields.io/badge/CLI%20Framework-Rich-000000.svg)](https://rich.readthedocs.io/en/stable/)
[![Interactive CLI: Inquirer](https://img.shields.io/badge/Interactive%20CLI-Inquirer-blue.svg)](https://github.com/magmax/python-inquirer)
[![Image Processing: Pillow](https://img.shields.io/badge/Image%20Processing-Pillow-5C6BC0.svg)](https://python-pillow.org/)
[![Database: SQLite](https://img.shields.io/badge/Database-SQLite-336791.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dunamismax/python-workspace/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/dunamismax/python-workspace/pulls)
[![GitHub Stars](https://img.shields.io/github/stars/dunamismax/python-workspace?style=social)](https://github.com/dunamismax/python-workspace/stargazers)

---

## Table of Contents

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Getting Started](#getting-started)
- [Projects Overview](#projects-overview)
- [Development Workflow](#development-workflow)
- [Scripts & Automation](#scripts--automation)
- [Contributing](#contributing)
- [Connect](#connect)
- [License](#license)

---

## Developer Resources

For comprehensive documentation, guides, and resources related to this monorepo, please visit the [docs folder](https://github.com/dunamismax/python-workspace/blob/main/docs/README.md). (Note: `docs` folder is not yet implemented but can be added here.)

---

## Introduction

This monorepo serves as a centralized hub for various Python applications and shared libraries. Each project within this repository is designed to be independent and self-contained, ensuring maximum isolation and flexibility for deployment, while benefiting from a unified development environment and shared tooling. This structure promotes code reusability, consistent practices, and simplified dependency management across diverse Python projects.

---

## Repository Structure

The repository is organized to support a scalable and maintainable monorepo architecture. Below is a detailed look at the directory structure.

<details>
<summary><strong>Click to expand repository layout</strong></summary>

```sh
python-workspace/
├── apps/                         # Directory for independent Python applications
│   ├── cli_launcher/             # A CLI tool to launch other applications
│   │   ├── requirements.txt      # Dependencies for the launcher (e.g., inquirer)
│   │   └── src/
│   │       └── cli_launcher/
│   │           ├── __init__.py
│   │           └── main.py       # Main script for the launcher
│   ├── file_butler/              # Command-Line Interface (CLI) tool for file organization
│   │   ├── launcher_config.json  # Configuration for the CLI launcher
│   │   ├── requirements.txt      # Dependencies (e.g., click)
│   │   └── src/
│   │       └── file_butler/
│   │           ├── __init__.py
│   │           └── main.py       # Main script for the file butler CLI
│   ├── job_scraper/              # Web scraping and data collection application
│   │   ├── launcher_config.json  # Configuration for the CLI launcher
│   │   ├── requirements.txt      # Dependencies (e.g., requests, beautifulsoup4)
│   │   └── src/
│   │       └── job_scraper/
│   │           ├── __init__.py
│   │           └── scraper.py    # Main script for the job scraper
│   ├── todo_api/                 # Backend Web Service (CRUD API)
│   │   ├── launcher_config.json  # Configuration for the CLI launcher
│   │   ├── requirements.txt      # Dependencies (e.g., fastapi, uvicorn, SQLAlchemy)
│   │   └── src/
│   │       └── todo_api/
│   │           ├── __init__.py
│   │           └── main.py       # Main script for the FastAPI service
│   ├── image_optimizer/          # System Automation and Scripting (Image Optimization)
│   │   ├── launcher_config.json  # Configuration for the CLI launcher
│   │   ├── requirements.txt      # Dependencies (e.g., Pillow)
│   │   └── src/
│   │       └── image_optimizer/
│   │           ├── __init__.py
│   │           └── main.py       # Main script for the image optimizer
├── libs/                         # Directory for shared libraries and packages
│   ├── database_utils/           # Utility functions for database interactions
│   │   ├── requirements.txt      # Dependencies (if any, e.g., for a specific DB driver)
│   │   └── src/
│   │       └── database_utils/
│   │           ├── __init__.py
│   │           └── db_connector.py # Functions for database connections
│   ├── image_processing/         # Utility functions for image manipulation
│   │   ├── requirements.txt      # Dependencies (if any, e.g., Pillow if not in app)
│   │   └── src/
│   │       └── image_processing/
│   │           ├── __init__.py
│   │           └── image_utils.py # Functions for image resizing, compression
├── scripts/                      # Utility scripts for monorepo management
│   └── run_tests.sh              # Runs tests across all applications
├── .gitignore                    # Git ignore file
├── pyproject.toml                # Monorepo-level tooling configuration (Black, Ruff, Pytest)
├── README.md                     # Monorepo root README
└── python-workspace-image.png    # Placeholder image for the README
```

</details>

---

## Tech Stack

This monorepo leverages a modern Python stack, optimized for performance and developer experience, with a focus on practical applications.

### I. Core Infrastructure & Backend

- **Programming Language:** [Python](https://www.python.org/) (3.9+)
- **Dependency Management:** `pip` with `requirements.txt`
- **Virtual Environments:** `venv`
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) (for `todo_api`)
- **Database:** [SQLite](https://www.sqlite.org/docs.html) (for `todo_api`)
- **HTTP Requests:** [Requests](https://requests.readthedocs.io/en/latest/) (for `job_scraper`)
- **HTML Parsing:** [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (for `job_scraper`)

### II. CLI & Automation

- **CLI Framework:** [Rich](https://rich.readthedocs.io/en/stable/)
- **Interactive CLI:** [Inquirer](https://github.com/magmax/python-inquirer)
- **Image Processing:** [Pillow](https://python-pillow.org/) (for `image_optimizer` and `libs/image_processing`)

---

## Quick Start

Get up and running with the monorepo:

```bash
# Clone the repository
git clone https://github.com/dunamismax/python-workspace.git
cd python-workspace

# Setup all projects (creates venvs, installs dependencies)
./scripts/setup_project.sh

# Run the CLI Launcher to select and run an application
./run_launcher.sh
```

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/) (Python 3.12+ recommended for latest features)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pyenv** (Recommended for managing Python versions) - [pyenv installation guide](https://github.com/pyenv/pyenv#installation)

### Detailed Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/python-workspace.git
   cd python-workspace
   ```

2. **Environment Setup**

   Run the automated setup script:

   ```bash
   ./scripts/setup_project.sh
   ```

   This script will:

   - Ensure `pyenv` is initialized (if installed).
   - Create a Python virtual environment (`.venv`) within each application and library directory.
   - Install all Python dependencies listed in each project's `requirements.txt` file.

3. **Running Applications**

   Use the `cli_launcher` to interactively select and run any application:

   ```bash
   ./run_launcher.sh
   ```

   Alternatively, you can manually activate an app's virtual environment and run its main script:

   ```bash
   cd apps/your_app_name
   source .venv/bin/activate
   python -m your_app_name.main # or relevant entry point
   deactivate
   ```

---

## Projects Overview

This monorepo hosts several independent Python applications, each demonstrating different functionalities and leveraging shared libraries.

### [CLI Launcher](apps/cli_launcher) - Interactive Application Runner

A central command-line tool that scans the `apps/` directory, lists detected applications, and allows the user to select and run any application. It automatically handles virtual environment activation and dependency installation for the chosen app.

### [File Butler](apps/file_butler) - Command-Line Interface (CLI) Tool

A practical utility that organizes files in a specified directory into subdirectories based on their file type (e.g., `.pdf` to `Documents/`, `.jpg` to `Images/`).

**Example Usage (via CLI Launcher):**
Select `file_butler` and provide a directory path (e.g., `/tmp/my_downloads`).

### [Job Scraper](apps/job_scraper) - Web Scraping and Data Collection

A script designed to scrape job listings from a specified job board website. It extracts information like job title, company name, and application link, saving the data to a CSV file. Uses `Requests` for HTTP requests and `Beautiful Soup 4` for HTML parsing.

**Example Usage (via CLI Launcher):**
Select `job_scraper`. It will run and create a `jobs.csv` file in its directory.

### [To-Do List API](apps/todo_api) - Backend Web Service (CRUD API)

A simple REST API built with `FastAPI` that allows users to manage a to-do list. It provides endpoints for creating, reading, updating, and deleting tasks, with data persistently stored in a SQLite database. This application demonstrates the use of the `libs/database_utils` shared library.

**Example Usage (via CLI Launcher):**
Select `todo_api`. The API will start on `http://127.0.0.1:8000`. Access `http://127.0.0.1:8000/docs` for API documentation.

### [Image Optimizer](apps/image_optimizer) - System Automation and Scripting

A script that scans a folder for images, resizes them to a maximum dimension, and compresses them to reduce file size, creating optimized, web-ready versions. This application demonstrates the use of the `libs/image_processing` shared library and `Pillow` for image manipulation.

**Example Usage (via CLI Launcher):**
Select `image_optimizer`. It will create a dummy image and process it, saving optimized versions to an `output_images` folder.

---

## Development Workflow

### Daily Development

1. **Activate Environment (Optional, for specific app development)**

   If you are working on a single application, you can `cd` into its directory and activate its virtual environment:

   ```bash
   cd apps/your_app_name
   source .venv/bin/activate
   ```
   Deactivate with `deactivate`.

2. **Run Applications**

   Use the `cli_launcher` for a streamlined experience:

   ```bash
   python -m apps.cli_launcher.src.cli_launcher.main
   ```

### Making Changes

1. **Install/Update Dependencies**

   If you modify a `requirements.txt` file, or add new dependencies, re-run the setup script:

   ```bash
   ./scripts/setup_project.sh
   ```

2. **Testing**

   Run tests for all applications:

   ```bash
   ./scripts/run_tests.sh
   ```

   Or run tests for a specific application (after activating its venv):

   ```bash
   cd apps/your_app_name
   source .venv/bin/activate
   pytest # Assuming pytest is installed in the venv
   deactivate
   ```

### Code Quality

- **Linting**: `ruff check .` (configured via root `pyproject.toml`)
- **Formatting**: `black .` (configured via root `pyproject.toml`)

---

## Scripts & Automation

The monorepo includes several automation scripts to streamline development:

### Setup & Installation

- **`setup_project.sh`** - Complete automated setup
  - Creates virtual environments for all apps and libs.
  - Installs all dependencies from `requirements.txt` files.
  - Ensures `pyenv` is initialized for correct Python version usage.

---

## Contributing

Contributions are welcome! Please feel free to fork the repository, create a feature branch, and open a pull request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Connect

Connect with the author, **dunamismax**, on:

- **Twitter:** [@dunamismax](https://twitter.com/dunamismax)
- **Bluesky:** [@dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
- **Reddit:** [u/dunamismax](https://www.reddit.com/user/dunamismax)
- **Discord:** `dunamismax`
- **Signal:** `dunamismax.66`

---

## License

This repository is licensed under the **MIT License**. See the `LICENSE` file for more details.