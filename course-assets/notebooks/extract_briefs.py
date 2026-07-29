#!/usr/bin/env python3
"""Extract source-faithful Markdown briefs from AI Bootcamp notebooks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


EXERCISE_RE = re.compile(r"\b(exercise|todo|your turn|task|challenge)\b", re.I)
IMPORT_RE = re.compile(
    r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE
)


def text(value: Any) -> str:
    if isinstance(value, list):
        return "".join(str(part) for part in value)
    return str(value or "")


def output_text(output: dict[str, Any]) -> str:
    output_type = output.get("output_type")
    if output_type == "stream":
        return text(output.get("text"))
    if output_type in {"execute_result", "display_data"}:
        data = output.get("data", {})
        for mime in ("text/plain", "text/markdown", "text/html"):
            if mime in data:
                return text(data[mime])
    if output_type == "error":
        traceback = output.get("traceback", [])
        return "\n".join(str(line) for line in traceback)
    return ""


def heading_lines(markdown: str) -> list[str]:
    return [
        line.strip()
        for line in markdown.splitlines()
        if re.match(r"^#{1,6}\s+\S", line.strip())
    ]


def render_notebook(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    headings: list[str] = []
    exercises: list[str] = []
    imports: set[str] = set()

    for cell in cells:
        source = text(cell.get("source"))
        if cell.get("cell_type") == "markdown":
            headings.extend(heading_lines(source))
            if EXERCISE_RE.search(source):
                exercises.append(source.strip().splitlines()[0])
        elif cell.get("cell_type") == "code":
            for match in IMPORT_RE.finditer(source):
                imports.add(match.group(1) or match.group(2))
            if EXERCISE_RE.search(source) or re.search(r"\bpass\s*(?:#.*)?$", source, re.M):
                first_line = next(
                    (line.strip() for line in source.splitlines() if line.strip()),
                    "Code exercise",
                )
                exercises.append(first_line)

    lines = [
        f"# Source Brief: {path.stem}",
        "",
        f"- Source notebook: `{path.name}`",
        f"- Notebook format: {notebook.get('nbformat')}.{notebook.get('nbformat_minor')}",
        f"- Cell count: {len(cells)}",
        f"- Code cells: {sum(c.get('cell_type') == 'code' for c in cells)}",
        f"- Markdown cells: {sum(c.get('cell_type') == 'markdown' for c in cells)}",
        f"- Imported packages: {', '.join(sorted(imports)) if imports else 'none detected'}",
        "",
        "## Source Headings",
        "",
    ]
    lines.extend(f"- {heading}" for heading in headings)
    if not headings:
        lines.append("- none")

    lines.extend(["", "## Source Exercises and Incomplete Cells", ""])
    lines.extend(f"- {item}" for item in exercises)
    if not exercises:
        lines.append("- none explicitly labelled")

    lines.extend(["", "## Cells in Source Order", ""])
    for index, cell in enumerate(cells, start=1):
        cell_type = cell.get("cell_type", "unknown")
        source = text(cell.get("source")).rstrip()
        lines.extend([f"### Cell {index:03d} - {cell_type}", ""])
        if cell_type == "markdown":
            lines.extend([source or "(empty markdown cell)", ""])
            continue

        language = "python" if cell_type == "code" else "text"
        lines.extend([f"```{language}", source, "```", ""])
        outputs = [
            rendered.rstrip()
            for output in cell.get("outputs", [])
            if (rendered := output_text(output)).strip()
        ]
        if outputs:
            lines.extend(["Output:", "", "```text", "\n\n".join(outputs), "```", ""])
        else:
            lines.extend(["Output: none stored", ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(args.source_dir.glob("[0-9][0-9].*.ipynb"))
    if not notebooks:
        raise SystemExit(f"No numbered notebooks found in {args.source_dir}")

    for notebook in notebooks:
        output = args.output_dir / f"{notebook.stem}.md"
        output.write_text(render_notebook(notebook), encoding="utf-8")
        print(f"{notebook.name} -> {output.name}")

    print(f"Extracted {len(notebooks)} notebook briefs")


if __name__ == "__main__":
    main()
