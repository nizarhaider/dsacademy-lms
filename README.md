# DS Academy LMS

DS Academy's self-hosted learning platform for practical data science and AI
education in English. This repository is a production-oriented fork of
[Frappe Learning](https://github.com/frappe/lms), pinned to LMS `v2.60.0` with
Frappe Framework `version-16`.

## Included

- Branded DS Academy learner and administrator experience
- 18-week flagship course with 18 topic lessons and 18 assessments
- 18 native quizzes with 54 questions
- 18 portfolio assignments with assessment rubrics
- 18 editable PowerPoint decks and LMS-ready PDFs
- English narration generated with the base OmniVoice model and its automatic voice
- 18 English lesson videos assembled from reviewed slides and narration
- Repeatable curriculum, branding, and settings seed
- Local Docker environment with MariaDB, Redis, workers, and websocket support
- Multi-architecture production image for AMD64 and ARM64
- AWS Lightsail deployment with backups and cost controls

## Local Setup

Requirements:

- Docker and Docker Compose
- At least 5 GB memory available to Docker
- Ports 8000 and 9000 available

Create local secrets:

```bash
cp .env.example .env
```

Set non-default values for `MARIADB_ROOT_PASSWORD` and `ADMIN_PASSWORD`, then
start the platform:

```bash
docker-compose --env-file .env --file docker/docker-compose.yml up --detach
```

The first start creates the bench, installs payments and LMS, creates the site,
builds the frontend, and runs the DS Academy seed. Open:

- LMS: <http://lms.localhost:8000/lms>
- Administrator login: the `ADMIN_PASSWORD` value from `.env`

Follow logs:

```bash
docker-compose --env-file .env --file docker/docker-compose.yml logs --follow frappe
```

Rerun the versioned seed:

```bash
docker-compose --env-file .env --file docker/docker-compose.yml exec \
  --workdir /home/frappe/frappe-bench frappe \
  bench --site lms.localhost execute lms.dsacademy.seed.seed_all
```

Audit curriculum counts:

```bash
docker-compose --env-file .env --file docker/docker-compose.yml exec \
  --workdir /home/frappe/frappe-bench frappe \
  bench --site lms.localhost execute lms.dsacademy.seed.get_seed_counts
```

Expected result:

```json
{"courses":1,"chapters":18,"lessons":36,"quizzes":18,"quiz_rows":54,"questions":54,"assignments":18}
```

## Curriculum Source

Reviewed files under
[`course-assets/slide-content`](course-assets/slide-content) are the source of
truth for lesson explanations, slide notes, narration, and guided notebooks.
[`lms/dsacademy/curriculum.py`](lms/dsacademy/curriculum.py) defines the LMS
course structure, quizzes, and assignments. [`lms/dsacademy/seed.py`](lms/dsacademy/seed.py)
applies both sources idempotently.

Generated slide sources and reviewed renders are under
[`course-assets/slides`](course-assets/slides). Learner-facing PowerPoints and
PDFs are published under `lms/public/course-media`.

## OmniVoice Narration

Narration uses the locally cached `k2-fsa/OmniVoice` base checkpoint and its
automatic voice. The generation call supplies lesson text and the documented
16-step inference setting, with no reference voice, style instruction, or
fine-tuned checkpoint. No paid API is used.

With the OmniVoice repository available next to this repository:

```bash
export OMNIVOICE_REPO=../OmniVoice
"$OMNIVOICE_REPO/.venv/bin/python" course-assets/audio/generate.py
```

The job is deterministic and resumable. Per-slide timing metadata and the
checksum manifest are written to `course-assets/audio`; normalized MP3 files
are published to the LMS media tree. Intermediate PCM files are temporary.

Audio generation uses Apple Silicon MPS. Stop the LMS containers first on
memory-constrained machines, then restart them after generation.

Assemble the reviewed slide renders and narrations into LMS-ready lesson videos:

```bash
python3 course-assets/video/generate.py
```

## Slides

The editable decks are generated with `@oai/artifact-tool` from
[`course-assets/slides/generate.mjs`](course-assets/slides/generate.mjs). Each
weekly deck contains 12 substantive slides, speaker notes, source blocks,
rendered PNGs, and layout inspection data.

Create the isolated Python environment used for contact sheets and PDFs:

```bash
python3 -m venv .venv-media
.venv-media/bin/pip install -r course-assets/slides/requirements.txt
```

Regenerate decks from the curriculum in an environment where
`@oai/artifact-tool` is available:

```bash
PYTHON="$PWD/.venv-media/bin/python" node course-assets/slides/generate.mjs
```

Publish reviewed decks as PowerPoint and PDF:

```bash
.venv-media/bin/python course-assets/slides/publish.py
```

After narration and video generation completes, verify every expected asset,
checksum, duration, stream, and codec:

```bash
python3 course-assets/validate.py
```

## Production

The GitHub workflow builds this fork for AMD64 and ARM64 and publishes:

```text
ghcr.io/nizarhaider/dsacademy-lms:stable
```

Production runs on the existing `small_3_1` Amazon Lightsail instance in
Mumbai. It keeps the application, database, Redis, proxy, and storage on one
USD 12/month bundle. See [`deploy/aws/README.md`](deploy/aws/README.md).

Production URL:

```text
https://learn.dsacademy.lk/lms
```

Deployments publish the `stable` GHCR image, update the existing Lightsail
Compose services, run migrations, and apply the idempotent curriculum seed.

## Security

- Never commit `.env`, database passwords, administrator passwords, or API keys.
- Replace all development credentials before exposing a site to the internet.
- Keep MariaDB and Redis private to the Docker network.
- Expose only ports 22, 80, and 443 on the production VM.
- Back up the site database and public/private files before upgrades.

## License

This project retains Frappe Learning's GNU Affero General Public License. See
[`license.txt`](license.txt). DS Academy curriculum and generated media remain
subject to their respective ownership and distribution terms.
