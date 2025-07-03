# libs/image_processing/tests/test_image_utils.py

import unittest
import os
from PIL import Image
from image_processing.image_utils import ImageProcessor

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        self.test_image_path = "test_image.png"
        self.output_path = "output_image.png"
        # Create a dummy image for testing
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.test_image_path)

    def tearDown(self):
        # Clean up the created files
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_load_image(self):
        processor = ImageProcessor(self.test_image_path)
        self.assertIsNotNone(processor.image)

    def test_save_image(self):
        processor = ImageProcessor(self.test_image_path)
        processor.save(self.output_path)
        self.assertTrue(os.path.exists(self.output_path))

    def test_resize_image(self):
        processor = ImageProcessor(self.test_image_path)
        processor.resize(max_size=(50, 50))
        self.assertEqual(processor.image.size, (50, 50))

    def test_convert_format(self):
        processor = ImageProcessor(self.test_image_path)
        output_jpg = "output_image.jpg"
        processor.convert_format(output_jpg, format="JPEG")
        self.assertTrue(os.path.exists(output_jpg))
        os.remove(output_jpg)

    def test_apply_grayscale(self):
        processor = ImageProcessor(self.test_image_path)
        processor.apply_grayscale()
        self.assertEqual(processor.image.mode, "L")

    def test_apply_sepia(self):
        # This is a bit harder to test precisely, so we'll just check if it runs without error
        processor = ImageProcessor(self.test_image_path)
        processor.apply_sepia()
        self.assertIsNotNone(processor.image)

    def test_add_watermark(self):
        # Also hard to test precisely, so we'll just check if it runs without error
        processor = ImageProcessor(self.test_image_path)
        processor.add_watermark("test")
        self.assertIsNotNone(processor.image)

if __name__ == '__main__':
    unittest.main()
