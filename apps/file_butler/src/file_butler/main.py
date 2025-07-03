import click
import os
import shutil

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def organize_files(directory):
    """Organizes files in the specified DIRECTORY into subdirectories based on file type."""
    click.echo(f"Organizing files in: {directory}")

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
                    click.echo(f"Moved '{filename}' to '{folder_name}/'")
                    moved = True
                    break
            if not moved:
                other_folder = os.path.join(directory, "Others")
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, filename))
                click.echo(f"Moved '{filename}' to 'Others/' (unclassified)")

    click.echo("File organization complete!")

if __name__ == '__main__':
    # Example usage: python -m file_butler.main /path/to/your/downloads
    # For testing, create a dummy directory and some files:
    # mkdir test_files
    # touch test_files/doc.pdf test_files/image.jpg test_files/audio.mp3 test_files/script.py test_files/unknown.xyz
    # python -m file_butler.main test_files
    organize_files()
