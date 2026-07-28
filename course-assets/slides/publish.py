"""Publish verified slide decks into Frappe's public course media tree."""

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PUBLIC_ROOT = ROOT.parents[1] / "lms" / "public" / "course-media"
GUIDED_NOTEBOOK_ROOT = ROOT.parent / "notebooks" / "guided"
WEEK_COUNT = 18


def publish_deck(deck_dir):
	destination = PUBLIC_ROOT / deck_dir.parent.name / deck_dir.name
	destination.mkdir(parents=True, exist_ok=True)
	shutil.copy2(deck_dir / "slides.pptx", destination / "slides.pptx")
	week_number = int(deck_dir.parent.name.removeprefix("module-"))
	guided_notebook = GUIDED_NOTEBOOK_ROOT / f"week-{week_number:02d}.ipynb"
	if not guided_notebook.exists():
		raise RuntimeError(f"Missing guided notebook: {guided_notebook}")
	shutil.copy2(guided_notebook, destination / "guided-lab.ipynb")

	image_paths = sorted((deck_dir / "rendered").glob("slide-*.png"))
	if not 10 <= len(image_paths) <= 12:
		raise RuntimeError(
			f"Expected 10–12 slide renders in {deck_dir}; found {len(image_paths)}"
		)
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
	decks = [
		ROOT / f"module-{week_number:02d}" / "lesson-01"
		for week_number in range(1, WEEK_COUNT + 1)
	]
	for deck in decks:
		if not deck.is_dir():
			raise RuntimeError(f"Missing approved curriculum deck: {deck}")
		publish_deck(deck)
		print(deck.relative_to(ROOT))
	print(f"Published {len(decks)} decks to {PUBLIC_ROOT}.")


if __name__ == "__main__":
	main()
