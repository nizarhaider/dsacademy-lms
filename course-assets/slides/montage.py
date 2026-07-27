"""Build compact seven-slide review sheets for generated decks."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
TILE_SIZE = (320, 180)
MONTAGE_SIZE = (1280, 360)


def build_montage(deck_dir):
	paths = sorted((deck_dir / "rendered").glob("slide-*.png"))
	if len(paths) != 7:
		raise RuntimeError(f"Expected seven slide renders in {deck_dir}")

	canvas = Image.new("RGB", MONTAGE_SIZE, "white")
	for index, path in enumerate(paths):
		with Image.open(path) as source:
			tile = source.convert("RGB").resize(TILE_SIZE, Image.Resampling.LANCZOS)
		canvas.paste(tile, ((index % 4) * TILE_SIZE[0], (index // 4) * TILE_SIZE[1]))
	canvas.save(deck_dir / "montage.webp", "WEBP", quality=90, method=6)


def main():
	decks = sorted(ROOT.glob("week-*/session-*"))
	for deck in decks:
		build_montage(deck)
	print(f"Built {len(decks)} slide montages.")


if __name__ == "__main__":
	main()
