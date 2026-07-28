"""Build compact review sheets for the approved 10–12-slide decks."""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
TILE_SIZE = (320, 180)
MONTAGE_SIZE = (1280, 720)
WEEK_COUNT = 18


def build_montage(deck_dir):
	paths = sorted((deck_dir / "rendered").glob("slide-*.png"))
	if not 10 <= len(paths) <= 12:
		raise RuntimeError(
			f"Expected 10–12 slide renders in {deck_dir}; found {len(paths)}"
		)

	canvas = Image.new("RGB", MONTAGE_SIZE, "white")
	for index, path in enumerate(paths):
		with Image.open(path) as source:
			tile = source.convert("RGB").resize(TILE_SIZE, Image.Resampling.LANCZOS)
		canvas.paste(tile, ((index % 4) * TILE_SIZE[0], (index // 4) * TILE_SIZE[1]))
	canvas.save(deck_dir / "montage.webp", "WEBP", quality=90, method=6)


def main():
	decks = (
		[Path(sys.argv[1]).resolve()]
		if len(sys.argv) > 1
		else [
			ROOT / f"module-{week_number:02d}" / "lesson-01"
			for week_number in range(1, WEEK_COUNT + 1)
		]
	)
	for deck in decks:
		build_montage(deck)
	print(f"Built {len(decks)} slide montages.")


if __name__ == "__main__":
	main()
