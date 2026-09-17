from collections import Counter
from pathlib import Path

text = Path("sample.txt").read_text(encoding="utf-8")
counts = Counter(text.lower().split())

for word, count in sorted(counts.items()):
    print(f"{word}: {count}")