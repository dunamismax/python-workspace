from PIL import Image
from rich.console import Console

console = Console()

def resize_image(image_path, output_path, max_size=(1280, 720)):
    """Resizes an image to fit within max_size while maintaining aspect ratio."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(output_path)
        console.print(f"[green]Resized[/green] [yellow]'{image_path}'[/yellow] to [cyan]'{output_path}'[/cyan]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error resizing {image_path}: {e}[/bold red]")
        return False

def compress_image(image_path, output_path, quality=85):
    """Compresses an image with a specified quality."""
    try:
        with Image.open(image_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        console.print(f"[green]Compressed[/green] [yellow]'{image_path}'[/yellow] to [cyan]'{output_path}'[/cyan]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error compressing {image_path}: {e}[/bold red]")
        return False

def optimize_image(image_path, output_path, max_size=(1280, 720), quality=85):
    """Optimizes an image by resizing and compressing it."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(output_path, optimize=True, quality=quality)
        console.print(f"[green]Optimized[/green] [yellow]'{image_path}'[/yellow] to [cyan]'{output_path}'[/cyan]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error optimizing {image_path}: {e}[/bold red]")
        return False
