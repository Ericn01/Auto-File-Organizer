import unittest

import parser_builder
from constants import DEFAULT_ARG_CONFIG


class TestParserBuilder(unittest.TestCase):
    def test_build_parser_parses_configured_args(self):
        arg_config = {
            "run": [
                {"flag": "--copy", "dest": "copy", "type": "bool", "default": False, "help": ""},
                {"flag": "--max-depth", "dest": "max_depth", "type": "int", "default": None, "help": ""},
                {"flag": "--ignore-extensions", "dest": "ignore_extensions", "type": "list", "default": None, "help": ""},
            ],
            "config": [],
        }
        parser = parser_builder.build_parser(arg_config)
        args = parser.parse_args(
            ["run", "src", "out", "--copy", "--max-depth", "2", "--ignore-extensions", ".tmp", ".log"]
        )
        self.assertTrue(args.copy)
        self.assertEqual(args.max_depth, 2)
        self.assertEqual(args.ignore_extensions, [".tmp", ".log"])

    def test_build_parser_includes_config_management_flags(self):
        parser = parser_builder.build_parser(DEFAULT_ARG_CONFIG)
        args = parser.parse_args(["config", "--reset"])
        self.assertTrue(args.reset_config)
        self.assertIsNone(args.set_default)
        self.assertFalse(hasattr(args, "source_dir"))
        self.assertFalse(hasattr(args, "output_dir"))

        args = parser.parse_args(["config", "--set-default", "max_depth.default", "3"])
        self.assertEqual(args.set_default, ["max_depth.default", "3"])

    def test_build_parser_parses_include_exclude_categories(self):
        parser = parser_builder.build_parser(DEFAULT_ARG_CONFIG)
        args = parser.parse_args(
            [
                "run",
                "src",
                "out",
                "--include-categories",
                "Images",
                "Videos",
                "--exclude-categories",
                "Videos",
            ]
        )
        self.assertEqual(args.include_categories, ["Images", "Videos"])
        self.assertEqual(args.exclude_categories, ["Videos"])
