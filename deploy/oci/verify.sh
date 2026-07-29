#!/usr/bin/env bash
set -euo pipefail

SITE_URL="${SITE_URL:-https://learn.dsacademy.lk}"

check_page() {
	local path="$1"
	curl --fail --location --silent --show-error \
		--output /dev/null "${SITE_URL}${path}"
	printf 'ok %s\n' "${path}"
}

check_media() {
	local path="$1"
	curl --fail --location --silent --show-error \
		--range 0-1023 --output /dev/null "${SITE_URL}${path}"
	printf 'ok %s\n' "${path}"
}

check_page "/"
check_page "/api/method/ping"
check_page "/lms"
check_page "/lms/courses/end-to-end-data-science-ai"
check_media "/assets/lms/images/dsacademy/course-cover.png"
check_media "/assets/lms/course-media/module-01/lesson-01/slides.pdf"
check_media "/assets/lms/course-media/module-01/lesson-01/narration-en.mp3"
check_media "/assets/lms/course-media/module-01/lesson-01/lesson-en.mp4"
check_media "/assets/lms/course-media/module-18/lesson-01/slides.pptx"
check_media "/assets/lms/course-media/module-18/lesson-01/narration-en.mp3"
check_media "/assets/lms/course-media/module-18/lesson-01/lesson-en.mp4"

printf 'DS Academy production smoke test passed for %s\n' "${SITE_URL}"
