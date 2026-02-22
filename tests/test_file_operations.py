import json
import os
import unittest
from pathlib import Path

import file_operations


class TestFileOperations(unittest.TestCase):
    def test_get_file_extension(self):
        self.assertEqual(file_operations.get_file_extension("a.txt"), ".txt")
        self.assertEqual(file_operations.get_file_extension("noext"), "")
        self.assertEqual(file_operations.get_file_extension("archive.tar.gz"), ".gz")

    def test_read_file_mappings_success(self):
        with self.subTest("valid json file returns dict"):
            with self._temp_dir() as tmp:
                mapping_path = tmp / "mapping.json"
                mapping_path.write_text(json.dumps({"media_mappings": {"Images": [".jpg"]}}))
                data = file_operations.read_file_mappings(str(mapping_path))
                self.assertIsInstance(data, dict)
                self.assertIn("media_mappings", data)

    def test_read_file_mappings_missing_or_bad_json(self):
        with self._temp_dir() as tmp:
            missing = tmp / "missing.json"
            self.assertIsNone(file_operations.read_file_mappings(str(missing)))

            bad = tmp / "bad.json"
            bad.write_text("{not json")
            self.assertIsNone(file_operations.read_file_mappings(str(bad)))

    def test_classify_file_case_insensitive_and_dot_normalization(self):
        mappings = {
            "Images": [".jpg", ".png"],
            "Docs": ["txt"],
        }
        self.assertEqual(file_operations.classify_file_extension("PHOTO.JPG", mappings), "Images")
        self.assertEqual(file_operations.classify_file_extension("readme.txt", mappings), "Docs")
        self.assertEqual(file_operations.classify_file_extension("noext", mappings), "Other")

    def test_create_mapping_folders_strict_raises(self):
        with self._temp_dir() as tmp:
            (tmp / "Images").mkdir()
            with self.assertRaises(file_operations.DirAlreadyExistsException):
                file_operations.create_mapping_folders({"Images": [".jpg"]}, parent_dir=str(tmp), strict=True)

    def test_create_mapping_folders_non_strict_creates_missing_and_other(self):
        with self._temp_dir() as tmp:
            (tmp / "Images").mkdir()
            file_operations.create_mapping_folders(
                {"Images": [".jpg"], "Docs": [".txt"]},
                parent_dir=str(tmp),
                strict=False,
                include_other=True,
            )
            self.assertTrue((tmp / "Images").is_dir())
            self.assertTrue((tmp / "Docs").is_dir())
            self.assertTrue((tmp / "Other").is_dir())

    def test_move_file_moves_or_copies(self):
        with self._temp_dir() as tmp:
            src = tmp / "a.txt"
            src.write_text("hello")
            dst = tmp / "b.txt"

            file_operations.move_file(str(src), str(dst), copy=True)
            self.assertTrue(src.exists())
            self.assertTrue(dst.exists())

        with self._temp_dir() as tmp:
            src = tmp / "a.txt"
            src.write_text("hello")
            dst = tmp / "b.txt"

            file_operations.move_file(str(src), str(dst), copy=False)
            self.assertFalse(src.exists())
            self.assertTrue(dst.exists())

    def test_walk_directory_respects_depth_ignore_and_size_filters(self):
        with self._temp_dir() as tmp:
            source = tmp / "source"
            output = tmp / "output"
            source.mkdir()
            output.mkdir()

            (source / "root.jpg").write_bytes(b"1234")
            (source / "skip.tmp").write_bytes(b"1234")
            nested = source / "nested"
            nested.mkdir()
            (nested / "nested.jpg").write_bytes(b"1234")
            (nested / "small.jpg").write_bytes(b"1")

            mapping = {"Images": [".jpg"]}
            file_operations.create_mapping_folders(mapping, parent_dir=str(output), strict=False, include_other=True)

            file_operations.walk_directory(
                dirpath=str(source),
                mapping_data=mapping,
                output_dir=str(output),
                copy=True,
                max_depth=0,
                min_size=2,
                ignore_extensions=[".tmp"],
            )

            # root.jpg copied; skip.tmp ignored; nested files excluded by depth; small.jpg excluded by min_size
            self.assertTrue((output / "Images" / "root.jpg").exists())
            self.assertFalse((output / "Other" / "skip.tmp").exists())
            self.assertFalse((output / "Images" / "nested.jpg").exists())
            self.assertFalse((output / "Images" / "small.jpg").exists())

    def test_walk_directory_creates_other_folder_on_demand(self):
        with self._temp_dir() as tmp:
            source = tmp / "source"
            output = tmp / "output"
            source.mkdir()
            output.mkdir()

            (source / "file.unknown").write_text("x")

            mapping = {"Images": [".jpg"]}
            # Deliberately do not create folders first.
            file_operations.walk_directory(
                dirpath=str(source),
                mapping_data=mapping,
                output_dir=str(output),
                copy=True,
            )
            self.assertTrue((output / "Other" / "file.unknown").exists())

    def test_filter_mapping_categories_include_and_exclude_with_warnings(self):
        mapping = {"Images": [".jpg"], "Videos": [".mp4"], "Docs": [".txt"]}
        warnings: list[str] = []

        filtered = file_operations.filter_mapping_categories(
            mapping,
            include_categories=["images", "Missing"],
            exclude_categories=["Videos", "also-missing"],
            warn=warnings.append,
        )
        self.assertEqual(set(filtered.keys()), {"Images"})
        self.assertTrue(any("include category 'Missing'" in w for w in warnings))
        self.assertTrue(any("exclude category 'also-missing'" in w for w in warnings))

    def test_filter_mapping_categories_supports_comma_separated_values(self):
        mapping = {"Images": [".jpg"], "Videos": [".mp4"], "Docs": [".txt"]}
        filtered = file_operations.filter_mapping_categories(
            mapping,
            include_categories=["Images,Videos"],
        )
        self.assertEqual(set(filtered.keys()), {"Images", "Videos"})

    @staticmethod
    def _temp_dir():
        # Small context manager wrapper to keep tests pathlib-only and readable.
        import tempfile
        from contextlib import contextmanager

        @contextmanager
        def _ctx():
            with tempfile.TemporaryDirectory() as d:
                yield Path(d)

        return _ctx()
