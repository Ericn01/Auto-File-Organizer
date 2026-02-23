import json
import unittest
from pathlib import Path

import configuration


class TestConfiguration(unittest.TestCase):
    def test_load_arg_config_creates_default_when_missing(self):
        with self._temp_dir() as tmp:
            cfg = tmp / "args.json"
            loaded = configuration.load_arg_config(filepath=str(cfg))
            self.assertEqual(loaded, configuration.DEFAULT_ARG_CONFIG)
            self.assertTrue(cfg.exists())

            on_disk = json.loads(cfg.read_text())
            self.assertEqual(on_disk, configuration.DEFAULT_ARG_CONFIG)

    def test_load_arg_config_bad_json_falls_back_to_default(self):
        with self._temp_dir() as tmp:
            cfg = tmp / "args.json"
            cfg.write_text("{bad json")
            loaded = configuration.load_arg_config(filepath=str(cfg))
            self.assertEqual(loaded, configuration.DEFAULT_ARG_CONFIG)

    def test_update_arg_config_updates_value(self):
        with self._temp_dir() as tmp:
            cfg = tmp / "args.json"
            configuration.save_arg_config(configuration.DEFAULT_ARG_CONFIG, filepath=str(cfg))

            configuration.update_arg_config("max_depth", "default", 3, filepath=str(cfg))
            loaded = configuration.load_arg_config(filepath=str(cfg))
            entry = next(e for e in loaded["run"] if e["dest"] == "max_depth")
            self.assertEqual(entry["default"], 3)

    def test_update_arg_config_raises_for_missing_dest(self):
        with self._temp_dir() as tmp:
            cfg = tmp / "args.json"
            configuration.save_arg_config(configuration.DEFAULT_ARG_CONFIG, filepath=str(cfg))
            with self.assertRaises(KeyError):
                configuration.update_arg_config("does_not_exist", "default", 1, filepath=str(cfg))

    @staticmethod
    def _temp_dir():
        import tempfile
        from contextlib import contextmanager

        @contextmanager
        def _ctx():
            with tempfile.TemporaryDirectory() as d:
                yield Path(d)

        return _ctx()
