import os
import sys
from rich.console import Console
from rich.progress import Progress

# Add the libs/image_processing/src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'libs', 'image_processing', 'src')))
from image_processing.image_utils import optimize_image

console = Console()

def process_images_in_folder(input_folder, output_folder, max_size=(1280, 720), quality=85):
    """Processes all images in a folder, optimizing them and saving to an output folder."""
    os.makedirs(output_folder, exist_ok=True)
    console.print(f"[bold green]Processing images in[/bold green] [cyan]'{input_folder}'[/cyan] [bold green]and saving to[/bold green] [cyan]'{output_folder}'[/cyan]")

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    with Progress(console=console) as progress:
        task = progress.add_task("[green]Optimizing images...[/green]", total=len(image_files))
        for filename in image_files:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            if optimize_image(input_path, output_path, max_size, quality):
                progress.update(task, advance=1, description=f"[green]Optimized[/green] [yellow]'{filename}'[/yellow]")
            else:
                progress.update(task, advance=1, description=f"[red]Failed to optimize[/red] [yellow]'{filename}'[/yellow]")

    console.print("[bold green]Image optimization complete![/bold green]")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        process_images_in_folder(input_folder, output_folder)
    else:
        console.print("[bold red]Usage: python -m image_optimizer.main <input_folder> <output_folder>[/bold red]")
        console.print("[bold yellow]Example: python -m image_optimizer.main input_images output_images[/bold yellow]")
