"""Build beginner-facing notebook guides from the reviewed slide Markdown."""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from lms.dsacademy.markdown_decks import load_markdown_slides

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "guided"
WEEK_COUNT = 18


def markdown(source):
	return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code(source):
	return {
		"cell_type": "code",
		"execution_count": None,
		"metadata": {},
		"outputs": [],
		"source": source.strip().splitlines(True),
	}


def fenced_blocks(section):
	return re.findall(r"```([^\n]*)\n(.*?)```", section, flags=re.DOTALL)


def source_urls(section):
	return re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", section)


def build_notebook(week_number):
	slides = load_markdown_slides(week_number)
	title = slides[0]["title"]
	outline = "\n".join(
		f"{item['number']}. {item['title']}" for item in slides
	)
	all_sources = []
	for item in slides:
		for url in source_urls(item["sections"]["Sources"]):
			if url not in all_sources:
				all_sources.append(url)

	cells = [
		markdown(
			f"""# Week {week_number:02d}: {title}

This notebook follows the reviewed Week {week_number} presentation. Read each concept and calculate the worked example before running its code.

## Lesson map

{outline}

Use the same reasoning loop throughout: **predict, run, inspect, explain**.
"""
		)
	]

	for item in slides:
		sections = item["sections"]
		cells.append(
			markdown(
				f"""## {item["number"]}. {item["title"]}

{sections["Learner-facing content"]}

### Work it out first

{sections["Worked example"]}

### Notebook bridge

{sections["Notebook connection"]}
"""
			)
		)
		blocks = fenced_blocks(sections["Code example"])
		if blocks:
			cells.append(
				markdown(
					"""Before running the next cell:

1. Identify every input value.
2. Predict the result or shape.
3. Run the cell.
4. Explain any difference between your prediction and the output.
"""
				)
			)
			cells.append(code(blocks[0][1]))
			if len(blocks) > 1:
				cells.append(
					markdown(
						f"""Expected output:

```text
{blocks[1][1].strip()}
```
"""
					)
				)

	lab = slides[-1]["sections"]
	cells.extend(
		[
			markdown(
				f"""## Guided lab

{lab["Learner-facing content"]}

### Reference result

{lab["Worked example"]}
"""
			),
			code(
				f"""# Guided lab workspace: Week {week_number:02d}
# Add only the imports needed for the current step.

# TODO 1: Prepare the smallest valid input.

# TODO 2: Apply the concept taught in this lesson.

# TODO 3: Display inspectable intermediate evidence.

# TODO 4: Compare the result with a hand calculation or stated requirement.
"""
			),
			markdown(
				"""## Weekly deliverable

Submit the completed guided lab with:

- your prediction before execution;
- intermediate values, shapes, metrics, or traces;
- one failed assumption and its correction;
- a plain-English explanation of the result;
- the source notebook section you are now ready to complete.
"""
			),
			markdown(
				"## Sources and source notebooks\n\n"
				+ "\n".join(f"- <{url}>" for url in all_sources)
			),
		]
	)
	return {
		"cells": cells,
		"metadata": {
			"kernelspec": {
				"display_name": "Python 3",
				"language": "python",
				"name": "python3",
			},
			"language_info": {"name": "python", "version": "3.12"},
			"dsacademy": {
				"week": week_number,
				"content_source": f"course-assets/slide-content/week-{week_number:02d}.md",
				"source_material": all_sources,
				"curriculum": "beginner-ai-18-week-v2",
			},
		},
		"nbformat": 4,
		"nbformat_minor": 5,
	}


def main():
	OUTPUT.mkdir(parents=True, exist_ok=True)
	expected = set()
	for week_number in range(1, WEEK_COUNT + 1):
		path = OUTPUT / f"week-{week_number:02d}.ipynb"
		expected.add(path)
		path.write_text(
			json.dumps(build_notebook(week_number), indent=2, ensure_ascii=False)
			+ "\n",
			encoding="utf-8",
		)
	for stale in OUTPUT.glob("week-*.ipynb"):
		if stale not in expected:
			stale.unlink()
	print(f"Built {len(expected)} guided notebooks in {OUTPUT}.")


if __name__ == "__main__":
	main()
