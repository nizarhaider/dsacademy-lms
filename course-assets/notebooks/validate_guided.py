"""Validate that guided notebooks are complete and Markdown-aligned."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GUIDED = ROOT / "guided"


def require(condition, message):
	if not condition:
		raise RuntimeError(message)


def main():
	for week in range(1, 19):
		path = GUIDED / f"week-{week:02d}.ipynb"
		require(path.exists(), f"missing {path}")
		notebook = json.loads(path.read_text(encoding="utf-8"))
		require(notebook["nbformat"] == 4, f"{path}: unsupported nbformat")
		require(len(notebook["cells"]) >= 20, f"{path}: too few guided cells")
		require(
			notebook["metadata"]["dsacademy"]["content_source"]
			== f"course-assets/slide-content/week-{week:02d}.md",
			f"{path}: wrong content source",
		)
		text = "\n".join(
			"".join(cell.get("source", [])) for cell in notebook["cells"]
		)
		for marker in ("## Lesson map", "## Guided lab", "## Weekly deliverable"):
			require(marker in text, f"{path}: missing {marker}")
		require("Expected output:" in text, f"{path}: missing expected output")
		require("http" in text, f"{path}: missing sources")
	print("Validated 18 Markdown-aligned guided notebooks.")


if __name__ == "__main__":
	main()
