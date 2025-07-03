# apps/image_optimizer/tests/test_main.py

import unittest
import os
from PIL import Image
from image_optimizer.main import process_images
import argparse

class TestImageOptimizer(unittest.TestCase):

    def setUp(self):
        self.input_dir = "test_input"
        self.output_dir = "test_output"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create a dummy image
        self.test_image = "test.png"
        img = Image.new('RGB', (200, 200), color = 'blue')
        img.save(os.path.join(self.input_dir, self.test_image))

    def tearDown(self):
        for d in [self.input_dir, self.output_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    os.remove(os.path.join(d, f))
                os.rmdir(d)

    def test_process_images(self):
        args = argparse.Namespace(
            input=self.input_dir,
            output=self.output_dir,
            max_width=100,
            max_height=100,
            quality=90,
            format=None,
            grayscale=False,
            sepia=False,
            watermark=None
        )
        process_images(args)
        
        output_path = os.path.join(self.output_dir, self.test_image)
        self.assertTrue(os.path.exists(output_path))
        with Image.open(output_path) as img:
            self.assertEqual(img.size, (100, 100))

if __name__ == '__main__':
    unittest.main()
