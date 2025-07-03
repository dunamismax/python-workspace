# apps/image_optimizer/src/image_optimizer/main.py

import argparse
import os

from image_processing.image_utils import ImageProcessor
from rich.console import Console
from rich.progress import Progress

console = Console()


def process_images(args):
    """Processes all images in a folder based on the provided arguments."""
    os.makedirs(args.output, exist_ok=True)
    console.print(f"[bold green]Processing images in[/bold green] [cyan]'{args.input}'[/cyan]")
    console.print(
        f"[bold green]Saving optimized images to[/bold green] [cyan]'{args.output}'[/cyan]"
    )

    image_files = [
        f
        for f in os.listdir(args.input)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ]

    with Progress(console=console) as progress:
        task = progress.add_task("[green]Optimizing images...[/green]", total=len(image_files))
        for filename in image_files:
            input_path = os.path.join(args.input, filename)
            output_path = os.path.join(args.output, filename)

            try:
                processor = ImageProcessor(input_path)
                processor.resize(max_size=(args.max_width, args.max_height))

                if args.grayscale:
                    processor.apply_grayscale()
                if args.sepia:
                    processor.apply_sepia()
                if args.watermark:
                    processor.add_watermark(args.watermark)

                if args.format:
                    base, _ = os.path.splitext(output_path)
                    output_path = f"{base}.{args.format.lower()}"
                    processor.convert_format(output_path, format=args.format)
                else:
                    processor.save(output_path, quality=args.quality)

                progress.update(
                    task,
                    advance=1,
                    description=f"[green]Processed[/green] [yellow]'{filename}'[/yellow]",
                )
            except Exception as e:
                progress.update(
                    task,
                    advance=1,
                    description=f"[red]Failed[/red] [yellow]'{filename}': {e}[/yellow]",
                )

    console.print("[bold green]Image processing complete![/bold green]")


def main():
    parser = argparse.ArgumentParser(
        description="An advanced image optimization and processing tool."
    )
    parser.add_argument("input", help="Input directory containing images to process.")
    parser.add_argument("output", help="Output directory to save processed images.")
    parser.add_argument("--max_width", type=int, default=1280, help="Maximum width for resizing.")
    parser.add_argument("--max_height", type=int, default=720, help="Maximum height for resizing.")
    parser.add_argument("--quality", type=int, default=85, help="Compression quality (1-100).")
    parser.add_argument(
        "--format", type=str, help="Convert images to a specific format (e.g., JPEG, PNG)."
    )
    parser.add_argument("--grayscale", action="store_true", help="Apply grayscale filter.")
    parser.add_argument("--sepia", action="store_true", help="Apply sepia filter.")
    parser.add_argument("--watermark", type=str, help="Add a text watermark to the images.")

    args = parser.parse_args()
    process_images(args)


if __name__ == "__main__":
    main()
