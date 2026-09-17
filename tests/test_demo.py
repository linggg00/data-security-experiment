import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "code" / "demo.py"
SPEC = importlib.util.spec_from_file_location("word_count_demo", SCRIPT)
demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class CountWordsTests(unittest.TestCase):
    def test_case_and_repeated_words(self):
        self.assertEqual(demo.count_words("Git CODEX git"), {"git": 2, "codex": 1})

    def test_english_and_chinese_punctuation(self):
        self.assertEqual(
            demo.count_words('Hello,world! “HELLO”；world。 (test) [test]'),
            {"hello": 2, "world": 2, "test": 2},
        )

    def test_punctuation_separates_adjacent_words(self):
        self.assertEqual(demo.count_words("one-two/three"), {"one": 1, "two": 1, "three": 1})

    def test_empty_and_punctuation_only(self):
        for text in ("", " \t\n", "!?，。—"):
            with self.subTest(text=text):
                self.assertEqual(demo.count_words(text), {})


class CommandLineTests(unittest.TestCase):
    def run_cli(self, directory, *args):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            cwd=directory, capture_output=True, text=True, encoding="utf-8",
        )

    def test_default_input_and_sorted_output(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "sample.txt").write_text("Git codex GIT!", encoding="utf-8")
            result = self.run_cli(directory)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "codex: 1\ngit: 2\n")

    def test_custom_input_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "custom input.txt"
            path.write_text("Zebra,apple APPLE", encoding="utf-8")
            result = self.run_cli(directory, str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "apple: 2\nzebra: 1\n")

    def test_missing_input(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli(directory, "missing.txt")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Input file not found: missing.txt", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
