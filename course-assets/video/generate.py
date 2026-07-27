"""Assemble narrated lesson videos from verified slide renders."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SLIDES_ROOT = REPO / "course-assets" / "slides"
AUDIO_ROOT = REPO / "lms" / "public" / "course-media"
OUTPUT_ROOT = AUDIO_ROOT
WEIGHTS = [0.15, 0.13, 0.18, 0.14, 0.15, 0.13, 0.12]


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--week", type=int)
	parser.add_argument("--session", type=int)
	parser.add_argument("--force", action="store_true")
	return parser.parse_args()


def duration_seconds(audio_path):
	result = subprocess.run(
		[
			"ffprobe",
			"-v",
			"error",
			"-show_entries",
			"format=duration",
			"-of",
			"json",
			str(audio_path),
		],
		check=True,
		capture_output=True,
		text=True,
	)
	return float(json.loads(result.stdout)["format"]["duration"])


def build_video(slide_paths, audio_path, output_path):
	duration = duration_seconds(audio_path)
	scene_durations = [duration * weight for weight in WEIGHTS]
	output_path.parent.mkdir(parents=True, exist_ok=True)

	with tempfile.NamedTemporaryFile(
		mode="w",
		suffix=".txt",
		encoding="utf-8",
		delete=False,
	) as concat_file:
		for slide_path, scene_duration in zip(slide_paths, scene_durations):
			escaped = str(slide_path).replace("'", "'\\''")
			concat_file.write(f"file '{escaped}'\n")
			concat_file.write(f"duration {scene_duration:.4f}\n")
		escaped_last = str(slide_paths[-1]).replace("'", "'\\''")
		concat_file.write(f"file '{escaped_last}'\n")
		concat_path = Path(concat_file.name)
	temporary_output = output_path.with_suffix(".tmp.mp4")

	try:
		temporary_output.unlink(missing_ok=True)
		subprocess.run(
			[
				"ffmpeg",
				"-hide_banner",
				"-loglevel",
				"error",
				"-y",
				"-f",
				"concat",
				"-safe",
				"0",
				"-i",
				str(concat_path),
				"-i",
				str(audio_path),
				"-vf",
				"scale=1280:720:force_original_aspect_ratio=decrease,"
				"pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white,"
				"format=yuv420p",
				"-r",
				"30",
				"-c:v",
				"libx264",
				"-preset",
				"medium",
				"-crf",
				"21",
				"-c:a",
				"aac",
				"-b:a",
				"128k",
				"-shortest",
				"-movflags",
				"+faststart",
				str(temporary_output),
			],
			check=True,
		)
		temporary_output.replace(output_path)
	finally:
		concat_path.unlink(missing_ok=True)
		temporary_output.unlink(missing_ok=True)


def main():
	args = parse_args()
	count = 0
	for week_dir in sorted(SLIDES_ROOT.glob("week-*")):
		week_number = int(week_dir.name.split("-")[1])
		if args.week and week_number != args.week:
			continue
		for session_dir in sorted(week_dir.glob("session-*")):
			session_number = int(session_dir.name.split("-")[1])
			if args.session and session_number != args.session:
				continue
			slides = sorted((session_dir / "rendered").glob("slide-*.png"))
			if len(slides) != 7:
				raise RuntimeError(f"Expected seven slide renders in {session_dir}")

			relative = Path(week_dir.name, session_dir.name)
			for language in ("en", "si"):
				audio = AUDIO_ROOT / relative / f"narration-{language}.mp3"
				if not audio.exists():
					continue
				output = OUTPUT_ROOT / relative / f"lesson-{language}.mp4"
				if output.exists() and not args.force:
					print(f"skip {output.relative_to(REPO)}")
					continue
				build_video(slides, audio, output)
				count += 1
				print(f"generated {output.relative_to(REPO)}")
	print(f"Generated {count} videos.")


if __name__ == "__main__":
	main()
