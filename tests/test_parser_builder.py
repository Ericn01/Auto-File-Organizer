import unittest

import parser_builder


class TestParserBuilder(unittest.TestCase):
    def test_build_parser_parses_configured_args(self):
        cfg = [
            {"flag": "--copy", "dest": "copy", "type": "bool", "default": False, "help": ""},
            {"flag": "--max-depth", "dest": "max_depth", "type": "int", "default": None, "help": ""},
            {"flag": "--ignore-extensions", "dest": "ignore_extensions", "type": "list", "default": None, "help": ""},
        ]
        parser = parser_builder.build_parser(cfg)
        args = parser.parse_args(
            ["src", "out", "--copy", "--max-depth", "2", "--ignore-extensions", ".tmp", ".log"]
        )
        self.assertTrue(args.copy)
        self.assertEqual(args.max_depth, 2)
        self.assertEqual(args.ignore_extensions, [".tmp", ".log"])

    def test_build_parser_includes_config_management_flags(self):
        parser = parser_builder.build_parser([])
        args = parser.parse_args(["--reset-config"])
        self.assertTrue(args.reset_config)
        self.assertIsNone(args.set_default)
        self.assertIsNone(args.source_dir)
        self.assertIsNone(args.output_dir)

        args = parser.parse_args(["--set-default", "max_depth.default", "3"])
        self.assertEqual(args.set_default, ["max_depth.default", "3"])

    def test_build_parser_parses_include_exclude_categories(self):
        parser = parser_builder.build_parser([])
        args = parser.parse_args(
            [
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
