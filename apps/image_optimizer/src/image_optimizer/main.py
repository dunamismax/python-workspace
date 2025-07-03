from PIL import Image
import os

# Assuming image_processing is in libs/image_processing/src/image_processing
# For demonstration, we'll include the logic directly or simulate import.
# from image_processing.image_utils import optimize_image as shared_optimize_image

def optimize_image(input_path, output_path, max_size=(1280, 720), quality=85):
    """Optimizes an image by resizing and compressing it."""
    try:
        with Image.open(input_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(output_path, optimize=True, quality=quality)
        print(f"Optimized '{input_path}' to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")
        return False

def process_images_in_folder(input_folder, output_folder, max_size=(1280, 720), quality=85):
    """Processes all images in a folder, optimizing them and saving to an output folder."""
    os.makedirs(output_folder, exist_ok=True)
    print(f"Processing images in '{input_folder}' and saving to '{output_folder}'")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            optimize_image(input_path, output_path, max_size, quality)

    print("Image optimization complete!")

if __name__ == "__main__":
    # Example usage:
    # 1. Create a dummy 'input_images' folder and put some images in it.
    # 2. Run: python -m image_optimizer.main
    # This will create an 'output_images' folder with optimized versions.

    # Create dummy input folder and a dummy image for demonstration
    dummy_input_folder = "input_images"
    dummy_output_folder = "output_images"
    os.makedirs(dummy_input_folder, exist_ok=True)

    try:
        # Create a simple dummy image using Pillow
        img = Image.new('RGB', (1920, 1080), color = 'red')
        img.save(os.path.join(dummy_input_folder, "dummy_large.png"))
        print(f"Created dummy image: {os.path.join(dummy_input_folder, "dummy_large.png")}")

        process_images_in_folder(dummy_input_folder, dummy_output_folder)
    except ImportError:
        print("Pillow library not found. Please install it: pip install Pillow")
    except Exception as e:
        print(f"An error occurred: {e}")
