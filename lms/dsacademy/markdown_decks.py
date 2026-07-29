"""Build presentation outlines directly from reviewed weekly Markdown."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTENT_ROOT = REPO / "course-assets" / "slide-content"
SECTION_NAMES = (
	"Teaching purpose",
	"Learner-facing content",
	"Worked example",
	"Code example",
	"Visual description",
	"Instructor notes",
	"Notebook connection",
	"Sources",
)


def _sections(slide_body):
	result = {}
	for name in SECTION_NAMES:
		match = re.search(
			rf"^### {re.escape(name)}\s*$\n(.*?)(?=^### |\Z)",
			slide_body,
			flags=re.MULTILINE | re.DOTALL,
		)
		result[name] = match.group(1).strip() if match else ""
	return result


def _plain(markdown):
	text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
	text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
	text = re.sub(r"[*_`#]+", "", text)
	text = re.sub(r"^\|?[\s:|-]+\|?\s*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
	text = re.sub(r"\s+", " ", text)
	return text.strip()


def _short(text, limit):
	text = _plain(text)
	if len(text) <= limit:
		return text
	trimmed = text[: limit + 1].rsplit(" ", 1)[0].rstrip(" ,;:")
	return trimmed


def _blocks(markdown):
	"""Return complete prose blocks while excluding fenced code and list items."""
	text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
	result = []
	for block in re.split(r"\n\s*\n", text):
		lines = [
			line.strip()
			for line in block.splitlines()
			if line.strip() and not re.match(r"^(?:[-*]|\d+\.)\s+", line.strip())
		]
		value = _plain(" ".join(lines))
		if value:
			result.append(value)
	return result


def _complete_excerpt(markdown, limit=240, blocks=2):
	"""Select whole source blocks instead of showing visibly truncated prose."""
	selected = []
	for block in _blocks(markdown):
		candidate = " ".join([*selected, block])
		if selected and len(candidate) > limit:
			break
		selected.append(block)
		if len(selected) >= blocks:
			break
	return " ".join(selected)


def _worked_result(markdown):
	blocks = _blocks(markdown)
	return blocks[-1] if blocks else _plain(markdown)


def _label(text, words=8, limit=65):
	plain = _plain(text)
	clause = re.split(r"[;:.]", plain, maxsplit=1)[0].strip()
	if clause and len(clause) <= limit:
		return clause
	label = " ".join(plain.split()[:words]).rstrip(" ,;:.")
	return _short(label, limit)


def _items(markdown, limit=4, item_limit=180):
	items = []
	for line in markdown.splitlines():
		match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.+)", line)
		if match:
			value = _plain(match.group(1))
			if value and value not in items:
				items.append(value)
	if items:
		return items[:limit]
	if len(items) < limit:
		for block in _blocks(markdown):
			for sentence in re.split(r"(?<=[.!?;])\s+", block):
				value = sentence.strip()
				if len(value) > item_limit:
					continue
				if len(value) >= 18 and value not in items:
					items.append(value)
				if len(items) >= limit:
					break
			if len(items) >= limit:
				break
	return items[:limit]


def _code_and_output(code_section):
	blocks = re.findall(r"```[^\n]*\n(.*?)```", code_section, flags=re.DOTALL)
	code = blocks[0].strip() if blocks else ""
	output = blocks[1].strip() if len(blocks) > 1 else ""
	if not output:
		match = re.search(
			r"Expected output:\s*(.+)$",
			code_section,
			flags=re.DOTALL,
		)
		output = _short(match.group(1), 450) if match else "Inspect the result."
	return code, output


def _source_urls(source_section):
	return re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", source_section)


def _notes(sections):
	return "\n\n".join(
		[
			sections["Learner-facing content"],
			f"[Worked Example]\n{sections['Worked example']}",
			f"[Visual Brief]\n{sections['Visual description']}",
			f"[Instructor Notes]\n{sections['Instructor notes']}",
			f"[Notebook Connection]\n{sections['Notebook connection']}",
		]
	)


def _narration(title, sections):
	core = _complete_excerpt(
		sections["Learner-facing content"],
		limit=380,
		blocks=2,
	)
	example = _worked_result(sections["Worked example"])
	if len(example) > 180:
		example = _complete_excerpt(
			sections["Worked example"],
			limit=180,
			blocks=2,
		)
	return f"{title}. {core} Worked example. {example}".strip()


def _slide_item(number, title, sections):
	learner = sections["Learner-facing content"]
	worked = sections["Worked example"]
	code, output = _code_and_output(sections["Code example"])
	sources = _source_urls(sections["Sources"])
	common = {
		"title": title,
		"narration": _narration(title, sections),
		"notes": _notes(sections),
		"sources": sources,
	}

	if number == 1:
		return {
			**common,
			"kind": "cover",
			"subtitle": _complete_excerpt(learner, limit=190, blocks=1),
		}
	if number == 12:
		return {
			**common,
			"kind": "lab",
			"body": title,
			"items": [
				_label(item)
				for item in _items(learner, limit=4, item_limit=180)
			],
		}
	if number == 11:
		risk_terms = (
			"mistake",
			"failure",
			"risk",
			"security",
			"hallucination",
			"assumption",
			"limit",
		)
		kind = "pitfalls" if any(term in title.lower() for term in risk_terms) else "checklist"
		return {
			**common,
			"kind": kind,
			"items": _items(
				f"{learner}\n{worked}",
				limit=3 if kind == "pitfalls" else 4,
				item_limit=150,
			),
		}
	if number == 10:
		return {
			**common,
			"kind": "checklist",
			"items": _items(f"{learner}\n{worked}", limit=4, item_limit=155),
		}
	if number in {3, 6, 9} and code:
		return {
			**common,
			"kind": "code_output",
			"code": code,
			"output": output,
			"takeaway": _worked_result(worked),
		}
	if number in {4, 8}:
		return {
			**common,
			"kind": "process",
			"body": _complete_excerpt(worked, limit=240, blocks=5),
			"items": [
				item
				for item in _items(learner, limit=4, item_limit=120)
			],
		}
	return {
		**common,
		"kind": "concept",
		"body": _complete_excerpt(learner, limit=300, blocks=3),
		"items": _items(f"{learner}\n{worked}", limit=6, item_limit=180),
		"index": number,
		"inverse": number in {5, 7},
	}


def load_markdown_slides(week_number):
	path = CONTENT_ROOT / f"week-{week_number:02d}.md"
	markdown = path.read_text(encoding="utf-8")
	matches = list(
		re.finditer(r"^## Slide (\d+) - (.+)$", markdown, flags=re.MULTILINE)
	)
	slides = []
	for index, match in enumerate(matches):
		end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
		number = int(match.group(1))
		title = match.group(2).strip()
		slides.append(
			{
				"number": number,
				"title": title,
				"sections": _sections(markdown[match.end():end]),
			}
		)
	if not 10 <= len(slides) <= 12:
		raise ValueError(f"{path}: expected 10–12 slides; found {len(slides)}")
	return slides


def build_markdown_slide_outline(week_number):
	return [
		_slide_item(item["number"], item["title"], item["sections"])
		for item in load_markdown_slides(week_number)
	]
