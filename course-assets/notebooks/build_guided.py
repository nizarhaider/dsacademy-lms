"""Build beginner-facing notebook guides from the approved curriculum."""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from lms.dsacademy.curriculum import WEEKS

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "guided"


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


def build_notebook(week_number, week):
	lesson = week["sessions"][0]
	concepts = "\n".join(f"- **{item}**" for item in lesson["concepts"])
	outcomes = "\n".join(f"- {item}" for item in lesson["outcomes"])
	terms = "\n".join(
		f"- `{name}`: {meaning}"
		for name, meaning in lesson["mechanism_terms"].items()
	)
	mistakes = "\n".join(f"- {item}" for item in lesson["common_mistakes"])
	deepening = "\n".join(f"{index}. {item}" for index, item in enumerate(lesson["deepening"], 1))
	cells = [
		markdown(
			f"""# Week {week_number:02d}: {lesson["title"]}

This guided notebook assumes **{lesson["prerequisites"]}**.

## Learning outcomes

{outcomes}
"""
		),
		markdown(
			f"""## Concepts before code

{concepts}

### Core mechanism

{lesson["mechanism"]}

### Terms and symbols

{terms}
"""
		),
		markdown(
			f"""## Worked example: predict first

{lesson["worked_example"]}

Before running the next cell:

1. Write the expected output.
2. Identify the input values.
3. Identify the transformation.
4. Explain what the result means.
"""
		),
		code(lesson["example"]["code"]),
		markdown(
			f"""### Check the evidence

Expected reference output:

```text
{lesson["example"]["output"]}
```

Verification requirement:

{lesson["example"]["verify"]}

Do not continue until you can explain why the output has this value or shape.
"""
		),
		markdown(
			f"""## Build the complete mental model

{deepening}

## Common mistakes

{mistakes}
"""
		),
		markdown(
			f"""## Guided lab

{lesson["lab"]}

Work in this order:

1. **Predict** what the next operation should do.
2. **Run** the smallest relevant section.
3. **Inspect** values, shapes, metrics, or traces.
4. **Explain** the observed result in plain language.
"""
		),
		code(
			f"""# Guided lab workspace: Week {week_number:02d}
# Add only the imports needed for the current step.

# TODO 1: Prepare the smallest valid input.

# TODO 2: Apply the concept taught in the slides.

# TODO 3: Print or display inspectable intermediate evidence.

# TODO 4: Check the result against the lesson's verification requirement.
"""
		),
		markdown(
			f"""## Continue into the source notebook

Source notebook:

<{lesson["source_material"]}>

Before running each source section, label it as one of:

- input or data preparation
- transformation or model operation
- evaluation or verification
- persistence or deployment

If a source cell uses an unfamiliar API, first identify the concept it implements.
"""
		),
		markdown(
			f"""## Weekly deliverable

{lesson["deliverable"]}

Include:

- your prediction before execution
- the observed evidence
- one mistake or failed assumption
- the correction
- a plain-language explanation of the final result
"""
		),
	]
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
				"source_material": lesson["source_material"],
				"curriculum": "beginner-ai-18-week-v1",
			},
		},
		"nbformat": 4,
		"nbformat_minor": 5,
	}


def main():
	OUTPUT.mkdir(parents=True, exist_ok=True)
	expected = set()
	for week_number, week in enumerate(WEEKS, 1):
		path = OUTPUT / f"week-{week_number:02d}.ipynb"
		expected.add(path)
		path.write_text(
			json.dumps(build_notebook(week_number, week), indent=2, ensure_ascii=False)
			+ "\n",
			encoding="utf-8",
		)
	for stale in OUTPUT.glob("week-*.ipynb"):
		if stale not in expected:
			stale.unlink()
	print(f"Built {len(expected)} guided notebooks in {OUTPUT}.")


if __name__ == "__main__":
	main()
