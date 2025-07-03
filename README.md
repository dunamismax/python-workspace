<p align="center">
  <img src="./python-workspace-image.png" alt="Python Monorepo logo" width="250"/>
</p>

<h1 align="center">Python Monorepo</h1>

<p align="center">
  A centralized repository for a diverse collection of Python applications and shared libraries, designed for efficient and scalable project management.
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Language-Python-3776AB.svg" alt="Language: Python"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Web%20Framework-FastAPI-009688.svg" alt="Web Framework: FastAPI"></a>
  <a href="https://rich.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/CLI%20Framework-Rich-000000.svg" alt="CLI Framework: Rich"></a>
  <a href="https://python-pillow.org/"><img src="https://img.shields.io/badge/Image%20Processing-Pillow-5C6BC0.svg" alt="Image Processing: Pillow"></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/Database-SQLite-336791.svg" alt="Database: SQLite"></a>
  <a href="https://github.com/dunamismax/python-workspace/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

---

## Introduction

This monorepo serves as a centralized hub for various Python applications and shared libraries. Each project is designed to be independent and self-contained, promoting code reusability, consistent practices, and simplified dependency management.

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dunamismax/python-workspace.git
    cd python-workspace
    ```

2.  **Set up the projects:**
    ```bash
    ./scripts/setup_project.sh
    ```

3.  **Run an application:**
    ```bash
    ./run_launcher.sh
    ```

---

## Repository Structure

```
python-workspace/
├── apps/
│   ├── cli_launcher/     # An interactive launcher for the other apps
│   ├── file_butler/      # A CLI tool for organizing files
│   ├── image_optimizer/  # A tool for optimizing and processing images
│   ├── job_scraper/      # A web scraper for job listings
│   ├── todo_api/         # A RESTful API for managing a to-do list
│   └── weather_cli/      # A CLI for checking the weather
├── libs/
│   ├── database_utils/   # Utilities for database interactions
│   ├── image_processing/ # Utilities for image manipulation
│   └── shared_utils/     # Shared utilities for file and web operations
├── scripts/
│   ├── run_tests.sh      # Runs tests for all projects
│   └── setup_project.sh  # Sets up the development environment
└── ...
```

---

## Projects Overview

### Applications

*   **CLI Launcher:** An interactive command-line tool to easily run any of the other applications in the monorepo.
*   **File Butler:** A powerful and customizable file organizer that sorts files into folders based on their type.
*   **Image Optimizer:** A versatile tool for resizing, compressing, and applying various filters to images.
*   **Job Scraper:** A web scraper for collecting job listings from Indeed.com.
*   **To-Do List API:** A RESTful API built with FastAPI for creating, reading, updating, and deleting tasks.
*   **Weather CLI:** A command-line tool for checking the current weather and a 5-day forecast for any location.

### Shared Libraries

*   **database_utils:** A library for managing SQLite database connections and operations.
*   **image_processing:** A library for performing a variety of image manipulation tasks.
*   **shared_utils:** A collection of shared utilities for file and web operations.

---

## Development

### Prerequisites

*   Python 3.9+
*   Git

### Setup

The `scripts/setup_project.sh` script will create a virtual environment for each application and library and install all the necessary dependencies.

### Running Tests

The `scripts/run_tests.sh` script will run all the tests for all the applications and libraries in the monorepo.

---

## Contributing

Contributions are welcome! Please feel free to fork the repository, create a feature branch, and open a pull request.

---

## License

This repository is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## Connect

Connect with the author, **dunamismax**, on:

- **Twitter:** [@dunamismax](https://twitter.com/dunamismax)
- **Bluesky:** [@dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)
- **Reddit:** [u/dunamismax](https://www.reddit.com/user/dunamismax)
- **Discord:** `dunamismax`
- **Signal:** `dunamismax.66`
