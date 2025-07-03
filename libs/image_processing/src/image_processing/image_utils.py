# libs/image_processing/src/image_processing/image_utils.py

from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

console = Console()


class ImageProcessor:
    """A class for performing various image processing operations."""

    def __init__(self, image_path: str):
        try:
            self.image = Image.open(image_path)
            self.image_path = image_path
            console.log(f"[green]Successfully loaded image:[/green] [cyan]{image_path}[/cyan]")
        except FileNotFoundError:
            console.log(f"[bold red]Error: Image file not found at {image_path}[/bold red]")
            raise
        except Exception as e:
            console.log(f"[bold red]Error opening image {image_path}: {e}[/bold red]")
            raise

    def save(self, output_path: str, quality: int = 85):
        """Saves the processed image to the specified path."""
        try:
            self.image.save(output_path, optimize=True, quality=quality)
            console.log(f"[green]Image saved to:[/green] [cyan]{output_path}[/cyan]")
        except Exception as e:
            console.log(f"[bold red]Error saving image to {output_path}: {e}[/bold red]")
            raise

    def resize(self, max_size: Tuple[int, int] = (1280, 720)):
        """Resizes the image to fit within max_size while maintaining aspect ratio."""
        self.image.thumbnail(max_size, Image.Resampling.LANCZOS)
        console.log(f"Image resized to fit within {max_size}.")
        return self

    def convert_format(self, output_path: str, format: str):
        """Converts the image to a different format."""
        try:
            self.image.save(output_path, format=format)
            console.log(f"Image converted to {format} and saved to {output_path}.")
        except Exception as e:
            console.log(f"[bold red]Error converting image format: {e}[/bold red]")
            raise

    def apply_grayscale(self):
        """Converts the image to grayscale."""
        self.image = self.image.convert("L")
        console.log("Applied grayscale filter.")
        return self

    def apply_sepia(self):
        """Applies a sepia filter to the image."""
        width, height = self.image.size
        pixels = self.image.load()

        for py in range(height):
            for px in range(width):
                r, g, b = self.image.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                self.image.putpixel((px, py), (tr, tg, tb))
        console.log("Applied sepia filter.")
        return self

    def add_watermark(
        self, text: str, font_path: str = None, font_size: int = 36, opacity: int = 128
    ):
        """Adds a text watermark to the image."""
        draw = ImageDraw.Draw(self.image)
        if font_path:
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                console.log(
                    f"[yellow]Warning: Font not found at {font_path}. Using default font.[/yellow]"
                )
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()

        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        x = self.image.width - text_width - 10
        y = self.image.height - text_height - 10

        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
        console.log(f"Added watermark: '{text}'")
        return self
