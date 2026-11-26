"""Entry point for the news-image-20261126 bounty.

The front page image is drawn by make_front_page.py and stored in this
repository as entry.png. This program copies that image to the output
path the harness reads, /output/entry.png. It does no network access
and writes the same bytes on every run.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
TARGET = Path("/output/entry.png")


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print(f"copied {SOURCE} -> {TARGET}")


if __name__ == "__main__":
    main()
