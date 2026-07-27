"""Generate deterministic English and Sinhala narration with local OmniVoice."""

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import snapshot_download

from lms.dsacademy.curriculum import WEEKS
from omnivoice import OmniVoice

REPO = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO / "course-assets" / "audio"
PUBLIC_ROOT = REPO / "lms" / "public" / "course-media"
MODEL_ID = "2broke2code/serendib-omnivoice-finetuned-v2"
MODEL_REVISION = "v2.0.0"
REFERENCE_TEXT = (
	"ඔබතුමාගේ ගිය මාසේ බිල් එක ටිකක් වැඩිවෙලා තියෙන්නේ Sir ගත්ත "
	"international call charges නිසා. Sirට ඕනෙ නම් මට පුළුවන් ඒකේ "
	"detailed report එකක් ඔබතුමාගේ registered email එකට එවන්න."
)


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--week", type=int)
	parser.add_argument("--session", type=int)
	parser.add_argument("--force", action="store_true")
	parser.add_argument("--steps", type=int, default=16)
	parser.add_argument("--speed", type=float, default=1.05)
	return parser.parse_args()


def resolve_model():
	override = os.environ.get("DSACADEMY_OMNIVOICE_MODEL")
	if override:
		return Path(override).expanduser().resolve()
	return Path(
		snapshot_download(
			MODEL_ID,
			revision=MODEL_REVISION,
			local_files_only=True,
		)
	)


def narration_text(session_data, language):
	if language == "en":
		return (
			f"Welcome to {session_data['title']}. "
			f"{session_data['narration_en']} "
			f"Your guided lab is to {session_data['lab'][0].lower() + session_data['lab'][1:]} "
			f"The portfolio evidence for this session is {session_data['deliverable'][0].lower() + session_data['deliverable'][1:]}"
		)
	return (
		f"{session_data['title']}. "
		f"{session_data['narration_si']} "
		f"Guided lab එක: {session_data['lab']} "
		f"Portfolio deliverable එක: {session_data['deliverable']}"
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


def generate_session(model, session_data, week_number, session_number, args):
	relative = Path(
		f"week-{week_number:02d}",
		f"session-{session_number:02d}",
	)
	languages = []
	texts = []
	results = []
	for language in ("en", "si"):
		wav_path = SOURCE_ROOT / relative / f"narration-{language}.wav"
		mp3_path = PUBLIC_ROOT / relative / f"narration-{language}.mp3"
		text = narration_text(session_data, language)
		if mp3_path.exists() and wav_path.exists() and not args.force:
			print(f"skip {relative}/narration-{language}.mp3", flush=True)
			results.append(metadata_for(mp3_path, wav_path, language, text))
		else:
			languages.append(language)
			texts.append(text)

	if not languages:
		return results

	seed = 20260727 + week_number * 100 + session_number * 10
	np.random.seed(seed)
	torch.manual_seed(seed)
	audios = model.generate(
		text=texts,
		language=languages,
		ref_audio=[str(model._dsacademy_reference_audio)] * len(languages),
		ref_text=[REFERENCE_TEXT] * len(languages),
		num_step=args.steps,
		speed=[args.speed] * len(languages),
	)

	for language, text, waveform in zip(languages, texts, audios):
		wav_path = SOURCE_ROOT / relative / f"narration-{language}.wav"
		mp3_path = PUBLIC_ROOT / relative / f"narration-{language}.mp3"
		wav_path.parent.mkdir(parents=True, exist_ok=True)
		if hasattr(waveform, "detach"):
			waveform = waveform.detach().cpu().numpy()
		sf.write(wav_path, waveform, model.sampling_rate)
		transcode_mp3(wav_path, mp3_path)
		print(f"generated {relative}/narration-{language}.mp3", flush=True)
		results.append(metadata_for(mp3_path, wav_path, language, text))
	return results


def metadata_for(mp3_path, wav_path, language, text):
	info = sf.info(wav_path)
	return {
		"language": language,
		"text": text,
		"duration_seconds": round(info.duration, 3),
		"sample_rate": info.samplerate,
		"wav_sha256": file_sha256(wav_path),
		"mp3_sha256": file_sha256(mp3_path),
		"wav": str(wav_path.relative_to(REPO)),
		"mp3": str(mp3_path.relative_to(REPO)),
	}


def needs_generation(week_number, session_number, args):
	relative = Path(
		f"week-{week_number:02d}",
		f"session-{session_number:02d}",
	)
	if args.force:
		return True
	return any(
		not (SOURCE_ROOT / relative / f"narration-{language}.wav").exists()
		or not (PUBLIC_ROOT / relative / f"narration-{language}.mp3").exists()
		for language in ("en", "si")
	)


def load_model():
	model_path = resolve_model()
	reference_audio = model_path / "samples" / "reference_033.wav"
	model = OmniVoice.from_pretrained(
		str(model_path),
		device_map="mps",
		dtype=torch.float16,
		load_asr=False,
	)
	model._dsacademy_reference_audio = reference_audio
	return model


def collect_manifest_items():
	items = []
	for week_index, week_data in enumerate(WEEKS, start=1):
		for session_index, session_data in enumerate(week_data["sessions"], start=1):
			relative = Path(
				f"week-{week_index:02d}",
				f"session-{session_index:02d}",
			)
			for language in ("en", "si"):
				wav_path = SOURCE_ROOT / relative / f"narration-{language}.wav"
				mp3_path = PUBLIC_ROOT / relative / f"narration-{language}.mp3"
				if not wav_path.exists() or not mp3_path.exists():
					continue
				item = metadata_for(
					mp3_path,
					wav_path,
					language,
					narration_text(session_data, language),
				)
				item.update({"week": week_index, "session": session_index})
				items.append(item)
	return items


def main():
	args = parse_args()
	os.environ.setdefault("HF_HUB_OFFLINE", "1")
	model = None

	manifest = {
		"model": MODEL_ID,
		"revision": MODEL_REVISION,
		"device": "mps",
		"steps": args.steps,
		"speed": args.speed,
		"items": [],
	}
	for week_index, week_data in enumerate(WEEKS, start=1):
		if args.week and week_index != args.week:
			continue
		for session_index, session_data in enumerate(week_data["sessions"], start=1):
			if args.session and session_index != args.session:
				continue
			if model is None and needs_generation(week_index, session_index, args):
				model = load_model()
			generate_session(
				model,
				session_data,
				week_index,
				session_index,
				args,
			)
			if torch.backends.mps.is_available():
				torch.mps.empty_cache()

	manifest["items"] = collect_manifest_items()
	SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
	manifest_path = SOURCE_ROOT / "manifest.json"
	manifest_path.write_text(
		json.dumps(manifest, ensure_ascii=False, indent=2),
		encoding="utf-8",
	)
	print(f"Wrote {manifest_path}", flush=True)


if __name__ == "__main__":
	main()
