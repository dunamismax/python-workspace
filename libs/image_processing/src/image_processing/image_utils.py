from PIL import Image

def resize_image(image_path, output_path, max_size=(1280, 720)):
    """Resizes an image to fit within max_size while maintaining aspect ratio."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(output_path)
        print(f"Resized '{image_path}' to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False

def compress_image(image_path, output_path, quality=85):
    """Compresses an image with a specified quality."""
    try:
        with Image.open(image_path) as img:
            img.save(output_path, optimize=True, quality=quality)
        print(f"Compressed '{image_path}' to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")
        return False
