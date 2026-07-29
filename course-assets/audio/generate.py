"""Generate deterministic English narration with the base OmniVoice model."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import snapshot_download

from lms.dsacademy.curriculum import WEEKS
from lms.dsacademy.deck_content import build_slide_outline
from omnivoice import OmniVoice

SOURCE_ROOT = REPO / "course-assets" / "audio"
PUBLIC_ROOT = REPO / "lms" / "public" / "course-media"
MODEL_ID = "k2-fsa/OmniVoice"
MODEL_REVISION = "c5fdb5ccb189668d56333f77ba2629f4cd7535f4"
NUM_STEPS = 16


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--module", "--week", dest="week", type=int)
	parser.add_argument("--week-from", type=int)
	parser.add_argument("--week-to", type=int)
	parser.add_argument("--lesson", "--session", dest="session", type=int)
	parser.add_argument("--force", action="store_true")
	args = parser.parse_args()
	if args.week and (args.week_from or args.week_to):
		parser.error("--week cannot be combined with --week-from or --week-to")
	if args.week_from and args.week_to and args.week_from > args.week_to:
		parser.error("--week-from cannot be greater than --week-to")
	return args


def resolve_model():
	override = os.environ.get("DSACADEMY_OMNIVOICE_MODEL")
	if override:
		return Path(override).expanduser().resolve()
	offline = os.environ.get("HF_HUB_OFFLINE") == "1"
	return Path(
		snapshot_download(
			MODEL_ID,
			revision=MODEL_REVISION,
			local_files_only=offline,
		)
	)


def slide_outline(week_number, session_number, week_data, session_data):
	return build_slide_outline(
		week_number,
		session_number,
		week_data,
		session_data,
	)


def narration_text(week_number, session_number, week_data, session_data):
	return "\n\n".join(
		slide["narration"]
		for slide in slide_outline(
			week_number,
			session_number,
			week_data,
			session_data,
		)
	)


def file_sha256(path):
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def transcode_mp3(wav_path, mp3_path):
	mp3_path.parent.mkdir(parents=True, exist_ok=True)
	subprocess.run(
		[
			"ffmpeg",
			"-hide_banner",
			"-loglevel",
			"error",
			"-y",
			"-i",
			str(wav_path),
			"-af",
			"loudnorm=I=-16:LRA=7:TP=-1.5",
			"-ar",
			"24000",
			"-ac",
			"1",
			"-b:a",
			"128k",
			str(mp3_path),
		],
		check=True,
	)


def audio_duration(path):
	result = subprocess.run(
		[
			"ffprobe",
			"-v",
			"error",
			"-show_entries",
			"format=duration",
			"-of",
			"default=noprint_wrappers=1:nokey=1",
			str(path),
		],
		check=True,
		capture_output=True,
		text=True,
	)
	return float(result.stdout.strip())


def generate_session(model, week_data, session_data, week_number, session_number, args):
	relative = Path(
		f"module-{week_number:02d}",
		f"lesson-{session_number:02d}",
	)
	timing_path = SOURCE_ROOT / relative / "timing-en.json"
	mp3_path = PUBLIC_ROOT / relative / "narration-en.mp3"
	slides = slide_outline(
		week_number,
		session_number,
		week_data,
		session_data,
	)
	text = "\n\n".join(slide["narration"] for slide in slides)
	if (
		mp3_path.exists()
		and timing_path.exists()
		and not args.force
	):
		print(f"skip {relative}/narration-en.mp3", flush=True)
		weights = json.loads(timing_path.read_text(encoding="utf-8"))["slide_weights"]
		return metadata_for(mp3_path, text, weights)

	waveforms = []
	sample_counts = []
	silence = np.zeros(round(model.sampling_rate * 0.35), dtype=np.float32)
	for slide_index, slide in enumerate(slides, start=1):
		np.random.seed(20260727)
		torch.manual_seed(20260727)
		# Base-model auto voice: no reference audio, style prompt, or fine-tuning.
		waveform = model.generate(
			text=slide["narration"],
			num_step=NUM_STEPS,
		)[0]
		if hasattr(waveform, "detach"):
			waveform = waveform.detach().cpu().numpy()
		waveform = np.asarray(waveform, dtype=np.float32).reshape(-1)
		waveforms.append(waveform)
		sample_count = len(waveform)
		if slide_index < len(slides):
			waveforms.append(silence)
			sample_count += len(silence)
		sample_counts.append(sample_count)
		print(
			f"generated {relative} slide {slide_index:02d}/{len(slides)}",
			flush=True,
		)

	waveform = np.concatenate(waveforms)
	total_samples = sum(sample_counts)
	weights = [round(count / total_samples, 8) for count in sample_counts]
	timing_path.parent.mkdir(parents=True, exist_ok=True)
	timing_path.write_text(
		json.dumps({"slide_weights": weights}, indent=2),
		encoding="utf-8",
	)
	with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temporary:
		wav_path = Path(temporary.name)
	try:
		sf.write(wav_path, waveform, model.sampling_rate)
		transcode_mp3(wav_path, mp3_path)
	finally:
		wav_path.unlink(missing_ok=True)
	print(f"generated {relative}/narration-en.mp3", flush=True)
	return metadata_for(mp3_path, text, weights)


def metadata_for(mp3_path, text, weights):
	return {
		"language": "en",
		"voice_mode": "base-model-auto",
		"text": text,
		"duration_seconds": round(audio_duration(mp3_path), 3),
		"sample_rate": 24000,
		"slide_count": len(weights),
		"slide_weights": weights,
		"mp3_sha256": file_sha256(mp3_path),
		"mp3": str(mp3_path.relative_to(REPO)),
	}


def needs_generation(week_number, session_number, args):
	relative = Path(
		f"module-{week_number:02d}",
		f"lesson-{session_number:02d}",
	)
	return (
		args.force
		or not (SOURCE_ROOT / relative / "timing-en.json").exists()
		or not (PUBLIC_ROOT / relative / "narration-en.mp3").exists()
	)


def load_model():
	model_path = resolve_model()
	device = (
		"cuda"
		if torch.cuda.is_available()
		else "mps"
		if torch.backends.mps.is_available()
		else "cpu"
	)
	return OmniVoice.from_pretrained(
		str(model_path),
		device_map=device,
		dtype=torch.float16 if device != "cpu" else torch.float32,
		load_asr=False,
	)


def collect_manifest_items():
	items = []
	for week_index, week_data in enumerate(WEEKS, start=1):
		for session_index, session_data in enumerate(week_data["sessions"], start=1):
			relative = Path(
				f"module-{week_index:02d}",
				f"lesson-{session_index:02d}",
			)
			timing_path = SOURCE_ROOT / relative / "timing-en.json"
			mp3_path = PUBLIC_ROOT / relative / "narration-en.mp3"
			if not mp3_path.exists() or not timing_path.exists():
				continue
			weights = json.loads(timing_path.read_text(encoding="utf-8"))["slide_weights"]
			item = metadata_for(
				mp3_path,
				narration_text(
					week_index,
					session_index,
					week_data,
					session_data,
				),
				weights,
			)
			item.update({"module": week_index, "lesson": session_index})
			items.append(item)
	return items


def main():
	args = parse_args()
	os.environ.setdefault("HF_HUB_OFFLINE", "1")
	model = None
	device = os.environ.get("DSACADEMY_GENERATION_DEVICE") or (
		"cuda"
		if torch.cuda.is_available()
		else "mps"
		if torch.backends.mps.is_available()
		else "cpu"
	)

	for week_index, week_data in enumerate(WEEKS, start=1):
		if args.week and week_index != args.week:
			continue
		if args.week_from and week_index < args.week_from:
			continue
		if args.week_to and week_index > args.week_to:
			continue
		for session_index, session_data in enumerate(week_data["sessions"], start=1):
			if args.session and session_index != args.session:
				continue
			if model is None and needs_generation(week_index, session_index, args):
				model = load_model()
			generate_session(
				model,
				week_data,
				session_data,
				week_index,
				session_index,
				args,
			)
			if torch.backends.mps.is_available():
				torch.mps.empty_cache()

	manifest = {
		"model": MODEL_ID,
		"revision": MODEL_REVISION,
			"voice_mode": "base-model-auto",
			"generation_call": "model.generate(text=text, num_step=16)",
			"generation_unit": "one automatic-voice call per slide",
			"diffusion_steps": NUM_STEPS,
			"device": device,
		"languages": ["en"],
		"items": collect_manifest_items(),
	}
	SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
	manifest_path = SOURCE_ROOT / "manifest.json"
	manifest_path.write_text(
		json.dumps(manifest, ensure_ascii=True, indent=2),
		encoding="utf-8",
	)
	print(f"Wrote {manifest_path}", flush=True)


if __name__ == "__main__":
	main()
