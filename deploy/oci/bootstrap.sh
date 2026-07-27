#!/usr/bin/env bash
set -euo pipefail

: "${SITE_NAME:?Set SITE_NAME, for example learn.dsacademy.lk}"
: "${LETSENCRYPT_EMAIL:?Set LETSENCRYPT_EMAIL}"

PROJECT_NAME="${PROJECT_NAME:-dsacademy_lms}"
IMAGE="${IMAGE:-ghcr.io/nizarhaider/dsacademy-lms}"
VERSION="${VERSION:-stable}"
INSTALLER="${INSTALLER:-$HOME/easy-install.py}"
DEPLOY_ROOT="${DEPLOY_ROOT:-$HOME/dsacademy-deploy}"
COMPOSE_FILE="${COMPOSE_FILE:-$HOME/${PROJECT_NAME}-compose.yml}"
export COMPOSE_FILE

if [[ ! -f "${INSTALLER}" ]]; then
	curl --fail --location --silent --show-error \
		https://frappe.io/easy-install.py \
		--output "${INSTALLER}"
fi

mkdir -p "${DEPLOY_ROOT}"
cd "${DEPLOY_ROOT}"

if [[ ! -d frappe_docker/.git ]]; then
	git clone --depth 1 https://github.com/frappe/frappe_docker.git
fi

case "$(uname -m)" in
	arm64|aarch64)
		# The upstream production Compose file currently pins application
		# services to amd64 even when the custom image is multi-architecture.
		sed -i.bak '/^[[:space:]]*platform: linux\/amd64$/d' \
			frappe_docker/compose.yaml
		;;
esac

python3 "${INSTALLER}" deploy \
	--project="${PROJECT_NAME}" \
	--email="${LETSENCRYPT_EMAIL}" \
	--image="${IMAGE}" \
	--version="${VERSION}" \
	--app=payments \
	--app=lms \
	--sitename="${SITE_NAME}"

docker compose --project-name "${PROJECT_NAME}" --file "${COMPOSE_FILE}" \
	exec --no-TTY backend \
	bench --site "${SITE_NAME}" execute lms.dsacademy.seed.seed_all
docker compose --project-name "${PROJECT_NAME}" --file "${COMPOSE_FILE}" \
	exec --no-TTY backend \
	bench --site "${SITE_NAME}" clear-cache

printf 'DS Academy LMS is available at https://%s/lms\n' "${SITE_NAME}"
