# apps/file_butler/tests/test_main.py

import unittest
import os
import json
from file_butler.main import FileButler

class TestFileButler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_organize_dir"
        self.config_file = "test_config.json"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create dummy files
        with open(os.path.join(self.test_dir, "test.txt"), "w") as f: f.write("txt")
        with open(os.path.join(self.test_dir, "test.jpg"), "w") as f: f.write("jpg")
        
        # Create dummy config
        with open(self.config_file, "w") as f:
            json.dump({"Documents": [".txt"], "Images": [".jpg"]}, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_dir)
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_organize_directory(self):
        butler = FileButler(self.config_file)
        butler.organize_directory(self.test_dir)
        
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "test.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Images", "test.jpg")))

    def test_organize_directory_dry_run(self):
        butler = FileButler(self.config_file)
        butler.organize_directory(self.test_dir, dry_run=True)
        
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Documents")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Images")))

if __name__ == '__main__':
    unittest.main()
