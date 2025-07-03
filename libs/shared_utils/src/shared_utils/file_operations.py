# libs/shared_utils/src/shared_utils/file_operations.py

import os
import shutil

from rich.console import Console

console = Console()


def move_file(source_path, destination_path, dry_run=False):
    """Moves a file from the source path to the destination path."""
    destination_dir = os.path.dirname(destination_path)
    try:
        if not dry_run:
            os.makedirs(destination_dir, exist_ok=True)
            shutil.move(source_path, destination_path)
        
        console.print(
            f"Moved [yellow]'{source_path}'[/yellow] to [green]'{destination_path}'[/green]"
        )
        return True
    except Exception as e:
        console.print(f"[bold red]Error moving file {source_path}: {e}[/bold red]")
        return False
