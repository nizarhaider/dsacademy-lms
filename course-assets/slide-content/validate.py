"""Validate the Markdown-first slide-content contract."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_SECTIONS = (
	"Teaching purpose",
	"Learner-facing content",
	"Worked example",
	"Code example",
	"Visual description",
	"Instructor notes",
	"Notebook connection",
	"Sources",
)
GENERIC_PHRASES = (
	"the vocabulary of this topic",
	"how the concept works",
	"build the complete mental model",
	"working concept that must be tied",
)


def slides(markdown):
	matches = list(
		re.finditer(r"^## Slide (\d+) - (.+)$", markdown, flags=re.MULTILINE)
	)
	result = []
	for index, match in enumerate(matches):
		end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
		result.append((int(match.group(1)), match.group(2).strip(), markdown[match.start():end]))
	return result


def validate(path):
	markdown = path.read_text(encoding="utf-8")
	assert "PRODUCTION AUTHORIZED" in markdown, f"{path}: not production authorized"
	assert not any(
		phrase in markdown.lower() for phrase in GENERIC_PHRASES
	), f"{path}: legacy generic language remains"
	deck = slides(markdown)
	assert 10 <= len(deck) <= 12, f"{path}: expected 10–12 slides; found {len(deck)}"
	assert [number for number, _, _ in deck] == list(
		range(1, len(deck) + 1)
	), f"{path}: slide numbers are not consecutive"
	for number, title, body in deck:
		assert title, f"{path}: slide {number} has no title"
		for section in REQUIRED_SECTIONS:
			assert (
				f"### {section}" in body
			), f"{path}: slide {number} is missing {section}"
		assert len(body.split()) >= 90, f"{path}: slide {number} is too thin"
		assert re.search(
			r"https?://", body.split("### Sources", 1)[1]
		), f"{path}: slide {number} has no source URL"
	return len(deck), len(markdown.split())


def main():
	paths = sorted(ROOT.glob("week-*.md"))
	assert paths, "No slide-content files found"
	for path in paths:
		slide_count, word_count = validate(path)
		print(f"{path.name}: {slide_count} slides, {word_count} words")


if __name__ == "__main__":
	main()
