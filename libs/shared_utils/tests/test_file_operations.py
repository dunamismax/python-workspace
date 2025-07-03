# libs/shared_utils/tests/test_file_operations.py

import unittest
import os
from shared_utils.file_operations import move_file

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.source_dir = "test_source"
        self.dest_dir = "test_dest"
        self.test_file = "test_file.txt"
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.dest_dir, exist_ok=True)
        with open(os.path.join(self.source_dir, self.test_file), "w") as f:
            f.write("test")

    def tearDown(self):
        if os.path.exists(os.path.join(self.source_dir, self.test_file)):
            os.remove(os.path.join(self.source_dir, self.test_file))
        if os.path.exists(os.path.join(self.dest_dir, self.test_file)):
            os.remove(os.path.join(self.dest_dir, self.test_file))
        if os.path.exists(self.source_dir):
            os.rmdir(self.source_dir)
        if os.path.exists(self.dest_dir):
            os.rmdir(self.dest_dir)

    def test_move_file(self):
        source_path = os.path.join(self.source_dir, self.test_file)
        dest_path = os.path.join(self.dest_dir, self.test_file)
        move_file(source_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))
        self.assertFalse(os.path.exists(source_path))

    def test_move_file_dry_run(self):
        source_path = os.path.join(self.source_dir, self.test_file)
        dest_path = os.path.join(self.dest_dir, self.test_file)
        move_file(source_path, dest_path, dry_run=True)
        self.assertTrue(os.path.exists(source_path))
        self.assertFalse(os.path.exists(dest_path))

if __name__ == '__main__':
    unittest.main()
