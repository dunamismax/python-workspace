# apps/file_butler/src/file_butler/main.py

import argparse
import json
import os

from rich.console import Console
from rich.table import Table
from shared_utils.file_operations import move_file

console = Console()


class FileButler:
    """A class for organizing files based on their type."""

    def __init__(self, config_path):
        self.file_types = self.load_config(config_path)

    def load_config(self, config_path):
        """Loads the file type configuration from a JSON file."""
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            console.print(
                f"[bold red]Error: Configuration file not found at {config_path}[/bold red]"
            )
            raise
        except json.JSONDecodeError:
            console.print(
                f"[bold red]Error: Invalid JSON in configuration file {config_path}[/bold red]"
            )
            raise

    def organize_directory(self, directory, recursive=False, dry_run=False):
        """Organizes the files in the specified directory."""
        console.print(
            f"[bold green]Starting file organization in:[/bold green] [cyan]{directory}[/cyan]"
        )
        if dry_run:
            console.print(
                "[bold yellow]Running in dry-run mode. No files will be moved.[/bold yellow]"
            )

        moved_files = {}
        if recursive:
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    self.organize_file(file_path, directory, moved_files, dry_run)
        else:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    self.organize_file(file_path, directory, moved_files, dry_run)

        self.print_summary(moved_files)

    def organize_file(self, file_path, base_directory, moved_files, dry_run):
        """Organizes a single file."""
        file_extension = os.path.splitext(file_path)[1].lower()
        moved = False
        for folder_name, extensions in self.file_types.items():
            if file_extension in extensions:
                destination_folder = os.path.join(base_directory, folder_name)
                destination_path = os.path.join(destination_folder, os.path.basename(file_path))
                if move_file(file_path, destination_path, dry_run):
                    moved_files.setdefault(folder_name, 0)
                    moved_files[folder_name] += 1
                moved = True
                break
        if not moved:
            other_folder = os.path.join(base_directory, "Others")
            destination_path = os.path.join(other_folder, os.path.basename(file_path))
            if move_file(file_path, destination_path, dry_run):
                moved_files.setdefault("Others", 0)
                moved_files["Others"] += 1

    def print_summary(self, moved_files):
        """Prints a summary of the file organization process."""
        if not moved_files:
            console.print("[bold yellow]No files were moved.[/bold yellow]")
            return

        table = Table(title="[bold green]File Organization Summary[/bold green]")
        table.add_column("Category", style="cyan")
        table.add_column("Files Moved", style="magenta", justify="right")

        for category, count in moved_files.items():
            table.add_row(category, str(count))

        console.print(table)


def main():
    parser = argparse.ArgumentParser(description="A powerful and customizable file organizer.")
    parser.add_argument("directory", help="The directory to organize.")
    parser.add_argument(
        "--config", default="file_types.json", help="Path to the JSON configuration file."
    )
    parser.add_argument(
        "--recursive", action="store_true", help="Organize files in subdirectories recursively."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate the organization without moving files."
    )

    args = parser.parse_args()

    try:
        butler = FileButler(args.config)
        butler.organize_directory(args.directory, args.recursive, args.dry_run)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")


if __name__ == "__main__":
    main()
