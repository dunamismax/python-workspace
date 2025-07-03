import os
import shutil
from rich.console import Console
from rich.text import Text

console = Console()

def organize_files(directory):
    """Organizes files in the specified DIRECTORY into subdirectories based on file type."""
    console.print(f"[bold green]Organizing files in:[/bold green] [cyan]{directory}[/cyan]")

    file_types = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv"],
        "Audio": [".mp3", ".wav", ".flac"],
        "Archives": [".zip", ".tar", ".gz", ".rar"],
        "Spreadsheets": [".xls", ".xlsx", ".csv"],
        "Presentations": [".ppt", ".pptx"],
        "Code": [".py", ".js", ".html", ".css", ".json", ".xml"],
    }

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            moved = False
            for folder_name, extensions in file_types.items():
                if file_extension in extensions:
                    destination_folder = os.path.join(directory, folder_name)
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(destination_folder, filename))
                    console.print(f"Moved [yellow]'{filename}'[/yellow] to [green]'{folder_name}/'[/green]")
                    moved = True
                    break
            if not moved:
                other_folder = os.path.join(directory, "Others")
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, filename))
                console.print(f"Moved [yellow]'{filename}'[/yellow] to [green]'Others/'[/green] (unclassified)")

    console.print("[bold green]File organization complete![/bold green]")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        organize_files(sys.argv[1])
    else:
        console.print("[bold red]Error: Please provide a directory to organize.[/bold red]")
