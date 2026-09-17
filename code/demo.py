import argparse
from collections import Counter
from pathlib import Path
import string
import unicodedata


def count_words(text: str) -> Counter:
    """Count lowercase words, treating punctuation as word separators."""
    normalized = "".join(
        " " if char in string.punctuation or unicodedata.category(char).startswith("P")
        else char
        for char in text.lower()
    )
    return Counter(normalized.split())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count words in a UTF-8 text file.")
    parser.add_argument(
        "input_file", nargs="?", default="sample.txt",
        help="input file path (default: sample.txt in the current directory)",
    )
    args = parser.parse_args(argv)
    path = Path(args.input_file)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        parser.error(f"Input file not found: {path}")
    except (OSError, UnicodeError) as exc:
        parser.error(f"Cannot read input file '{path}': {exc}")

    for word, count in sorted(count_words(text).items()):
        print(f"{word}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
