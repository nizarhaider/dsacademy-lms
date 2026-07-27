"""Publish verified slide decks into Frappe's public course media tree."""

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PUBLIC_ROOT = ROOT.parents[1] / "lms" / "public" / "course-media"


def publish_deck(deck_dir):
	destination = PUBLIC_ROOT / deck_dir.parent.name / deck_dir.name
	destination.mkdir(parents=True, exist_ok=True)
	shutil.copy2(deck_dir / "slides.pptx", destination / "slides.pptx")

	image_paths = sorted((deck_dir / "rendered").glob("slide-*.png"))
	if len(image_paths) != 7:
		raise RuntimeError(f"Expected seven slide renders in {deck_dir}")
	images = [Image.open(path).convert("RGB") for path in image_paths]
	try:
		first, *remaining = images
		first.save(
			destination / "slides.pdf",
			"PDF",
			save_all=True,
			append_images=remaining,
			resolution=144,
		)
	finally:
		for image in images:
			image.close()


def main():
	decks = sorted(ROOT.glob("week-*/session-*"))
	for deck in decks:
		publish_deck(deck)
		print(deck.relative_to(ROOT))
	print(f"Published {len(decks)} decks to {PUBLIC_ROOT}.")


if __name__ == "__main__":
	main()
