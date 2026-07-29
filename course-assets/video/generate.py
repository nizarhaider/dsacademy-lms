"""Assemble English lesson videos from approved slide renders and base-model audio."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SLIDES_ROOT = REPO / "course-assets" / "slides"
AUDIO_ROOT = REPO / "lms" / "public" / "course-media"
OUTPUT_ROOT = AUDIO_ROOT
TIMING_ROOT = REPO / "course-assets" / "audio"


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--module", "--week", dest="week", type=int)
	parser.add_argument("--lesson", "--session", dest="session", type=int)
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


def load_slide_weights():
	weights = {}
	for timing_path in TIMING_ROOT.glob("module-*/lesson-*/timing-en.json"):
		week = int(timing_path.parents[1].name.split("-")[1])
		session = int(timing_path.parent.name.split("-")[1])
		item = json.loads(timing_path.read_text(encoding="utf-8"))
		if not 10 <= len(item["slide_weights"]) <= 12:
			raise RuntimeError(f"Invalid timing metadata: {timing_path}")
		weights[(week, session)] = item["slide_weights"]
	return weights


def build_video(slide_paths, audio_path, output_path, weights):
	duration = duration_seconds(audio_path)
	total_weight = sum(weights)
	scene_durations = [duration * weight / total_weight for weight in weights]
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
				"10",
				"-c:v",
				"libx264",
				"-preset",
				"medium",
				"-crf",
				"24",
				"-tune",
				"stillimage",
				"-c:a",
				"aac",
				"-b:a",
				"128k",
				"-t",
				f"{duration:.3f}",
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
	weights_by_session = load_slide_weights()
	count = 0
	for week_dir in sorted(SLIDES_ROOT.glob("module-*")):
		week_number = int(week_dir.name.split("-")[1])
		if args.week and week_number != args.week:
			continue
		for session_dir in sorted(week_dir.glob("lesson-*")):
			session_number = int(session_dir.name.split("-")[1])
			if args.session and session_number != args.session:
				continue
			slides = sorted((session_dir / "rendered").glob("slide-*.png"))
			if not 10 <= len(slides) <= 12:
				raise RuntimeError(
					f"Expected 10–12 slide renders in {session_dir}; found {len(slides)}"
				)

			relative = Path(week_dir.name, session_dir.name)
			audio = AUDIO_ROOT / relative / "narration-en.mp3"
			if not audio.exists():
				raise RuntimeError(f"Missing English narration: {audio}")
			output = OUTPUT_ROOT / relative / "lesson-en.mp4"
			if output.exists() and not args.force:
				print(f"skip {output.relative_to(REPO)}")
				continue
			key = (week_number, session_number)
			if key not in weights_by_session:
				raise RuntimeError(f"Missing slide timing metadata for {key}")
			if len(weights_by_session[key]) != len(slides):
				raise RuntimeError(
					f"Slide/timing count mismatch for {key}: "
					f"{len(slides)} renders and {len(weights_by_session[key])} weights"
				)
			build_video(slides, audio, output, weights_by_session[key])
			count += 1
			print(f"generated {output.relative_to(REPO)}")
	print(f"Generated {count} videos.")


if __name__ == "__main__":
	main()
