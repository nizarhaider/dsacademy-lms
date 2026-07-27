#!/usr/bin/env bash
set -euo pipefail

: "${S3_BUCKET:?Set S3_BUCKET to the private production backup bucket}"

SITE_NAME="${SITE_NAME:-learn.dsacademy.lk}"
PROJECT_NAME="${PROJECT_NAME:-dsacademy_lms}"
COMPOSE_FILE="${COMPOSE_FILE:-$HOME/${PROJECT_NAME}-compose.yml}"
AWS_REGION="${AWS_REGION:-ap-south-1}"
AWS_CLI_IMAGE="${AWS_CLI_IMAGE:-amazon/aws-cli:latest}"
SITES_VOLUME="${SITES_VOLUME:-${PROJECT_NAME}_sites}"

compose=(
	docker compose
	--project-name "${PROJECT_NAME}"
	--file "${COMPOSE_FILE}"
)

"${compose[@]}" exec --no-TTY --interactive=false backend \
	bench --site "${SITE_NAME}" backup --with-files --compress

docker run --rm \
	--volume "${SITES_VOLUME}:/sites:ro" \
	--volume "${HOME}/.aws:/root/.aws:ro" \
	"${AWS_CLI_IMAGE}" \
	s3 sync \
	"/sites/${SITE_NAME}/private/backups" \
	"s3://${S3_BUCKET}/production" \
	--region "${AWS_REGION}" \
	--sse AES256 \
	--only-show-errors

printf 'Off-instance backup completed for %s\n' "${SITE_NAME}"
