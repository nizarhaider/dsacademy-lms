"""Validate the complete DS Academy lesson-media package."""

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from lms.dsacademy.curriculum import WEEKS
from lms.dsacademy.deck_content import build_slide_outline

AUDIO_ROOT = REPO / "course-assets" / "audio"
SLIDES_ROOT = REPO / "course-assets" / "slides"
PUBLIC_ROOT = REPO / "lms" / "public" / "course-media"


def sha256(path):
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def probe(path):
	result = subprocess.run(
		[
			"ffprobe",
			"-v",
			"error",
			"-show_streams",
			"-show_format",
			"-of",
			"json",
			str(path),
		],
		check=True,
		capture_output=True,
		text=True,
	)
	return json.loads(result.stdout)


def require(condition, message):
	if not condition:
		raise AssertionError(message)


def validate_audio(path):
	data = probe(path)
	audio = next(stream for stream in data["streams"] if stream["codec_type"] == "audio")
	duration = float(data["format"]["duration"])
	require(audio["sample_rate"] == "24000", f"{path}: expected 24 kHz audio")
	require(audio["channels"] == 1, f"{path}: expected mono audio")
	require(120 <= duration <= 900, f"{path}: implausible {duration:.2f}s duration")
	quality = subprocess.run(
		[
			"ffmpeg",
			"-hide_banner",
			"-nostats",
			"-i",
			str(path),
			"-af",
			"volumedetect,silencedetect=noise=-45dB:d=2",
			"-f",
			"null",
			"-",
		],
		check=True,
		capture_output=True,
		text=True,
	)
	peak_match = re.search(r"max_volume: ([-\d.]+) dB", quality.stderr)
	require(peak_match, f"{path}: peak level unavailable")
	peak = float(peak_match.group(1))
	require(-8 <= peak <= -1, f"{path}: unexpected {peak:.1f} dBFS peak")
	require("silence_duration:" not in quality.stderr, f"{path}: long silent section")
	return duration


def validate_video(path, audio_duration):
	data = probe(path)
	video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
	audio = next(stream for stream in data["streams"] if stream["codec_type"] == "audio")
	duration = float(data["format"]["duration"])
	require(video["codec_name"] == "h264", f"{path}: expected H.264")
	require(video["width"] == 1280 and video["height"] == 720, f"{path}: expected 720p")
	require(video["pix_fmt"] == "yuv420p", f"{path}: expected yuv420p")
	require(audio["codec_name"] == "aac", f"{path}: expected AAC")
	require(abs(duration - audio_duration) <= 1.5, f"{path}: audio/video duration mismatch")


def main():
	manifest_path = AUDIO_ROOT / "manifest.json"
	manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	require(manifest["model"] == "k2-fsa/OmniVoice", "expected base OmniVoice model")
	require(manifest["voice_mode"] == "base-model-auto", "expected automatic base voice")
	require(
		manifest["generation_call"] == "model.generate(text=text, num_step=16)",
		"voice generation must not include a style or reference prompt",
	)
	require(manifest["diffusion_steps"] == 16, "expected documented fast inference")
	require(manifest["languages"] == ["en"], "only English narration should be published")
	items = {
		(item["module"], item["lesson"], item["language"]): item
		for item in manifest["items"]
	}
	expected_lessons = sum(len(module["sessions"]) for module in WEEKS)
	require(
		len(items) == expected_lessons,
		f"manifest has {len(items)} items, expected {expected_lessons}",
	)

	for week, module in enumerate(WEEKS, start=1):
		for session in range(1, len(module["sessions"]) + 1):
			session_data = module["sessions"][session - 1]
			slide_count = len(
				build_slide_outline(week, session, module, session_data)
			)
			require(
				10 <= slide_count <= 12,
				f"module {week}, lesson {session}: expected 10–12 slides",
			)
			relative = Path(f"module-{week:02d}", f"lesson-{session:02d}")
			source = SLIDES_ROOT / relative
			public = PUBLIC_ROOT / relative
			require(
				len(list((source / "rendered").glob("slide-*.png"))) == slide_count,
				f"{relative}: expected {slide_count} slide renders",
			)
			pptx = public / "slides.pptx"
			pdf = public / "slides.pdf"
			require(pptx.stat().st_size > 0, f"{relative}: missing PowerPoint")
			require(pdf.stat().st_size > 0, f"{relative}: missing PDF")
			require(sha256(source / "slides.pptx") == sha256(pptx), f"{pptx}: unpublished source")
			with zipfile.ZipFile(pptx) as archive:
				require("ppt/presentation.xml" in archive.namelist(), f"{pptx}: structure")
				require(archive.testzip() is None, f"{pptx}: corrupt member")
				notes = [
					name
					for name in archive.namelist()
					if name.startswith("ppt/notesSlides/notesSlide") and name.endswith(".xml")
				]
				require(
					len(notes) == slide_count,
					f"{pptx}: expected {slide_count} speaker-note pages",
				)
				require(
					b"[Sources]" in b"".join(archive.read(name) for name in notes),
					f"{pptx}: missing source notes",
				)
			page_count = len(re.findall(rb"/Type\s*/Page(?!s)\b", pdf.read_bytes()))
			require(
				page_count == slide_count,
				f"{pdf}: expected {slide_count} pages, found {page_count}",
			)

			key = (week, session, "en")
			item = items[key]
			mp3 = REPO / item["mp3"]
			video = public / "lesson-en.mp4"
			for path in (mp3, video):
				require(path.stat().st_size > 0, f"missing {path}")
			require(not (public / "narration-si.mp3").exists(), f"{relative}: Sinhala audio")
			require(not (public / "lesson-si.mp4").exists(), f"{relative}: Sinhala video")
			require(sha256(mp3) == item["mp3_sha256"], f"{mp3}: checksum")
			require(item["sample_rate"] == 24000, f"{mp3}: manifest sample rate")
			require(item["slide_count"] == slide_count, f"{mp3}: slide count")
			require(
				len(item["slide_weights"]) == slide_count,
				f"{mp3}: timing weights",
			)
			require(len(item["text"]) > 1500, f"{mp3}: narration is too short")
			audio_duration = validate_audio(mp3)
			require(
				abs(audio_duration - item["duration_seconds"]) <= 0.2,
				f"{mp3}: manifest duration mismatch",
			)
			validate_video(video, audio_duration)

	print(
		f"Validated {expected_lessons} English narrations, videos, and 10–12-slide decks."
	)


if __name__ == "__main__":
	main()
