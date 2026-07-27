#!/usr/bin/env bash

set -euo pipefail

if [ ! -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Creating Frappe bench on ${FRAPPE_BRANCH}..."
    bench init \
        --frappe-branch "${FRAPPE_BRANCH}" \
        --ignore-exist \
        --skip-redis-config-generation \
        frappe-bench
fi

cd /home/frappe/frappe-bench

bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

if [ ! -e "apps/payments" ]; then
    bench get-app --branch version-15 payments
fi

if [ ! -e "apps/lms" ]; then
    bench get-app --soft-link lms /workspace
fi

uv pip install "setuptools<82" --python env/bin/python

if [ ! -d "sites/${SITE_NAME}" ]; then
    bench new-site "${SITE_NAME}" \
        --mariadb-root-password "${MARIADB_ROOT_PASSWORD}" \
        --admin-password "${ADMIN_PASSWORD}" \
        --no-mariadb-socket
fi

installed_apps="$(bench --site "${SITE_NAME}" list-apps)"

if ! grep -qx "payments" <<< "${installed_apps}"; then
    bench --site "${SITE_NAME}" install-app --force payments
fi

if ! grep -qx "lms" <<< "${installed_apps}"; then
    bench --site "${SITE_NAME}" install-app --force lms
fi

bench --site "${SITE_NAME}" set-config developer_mode 1
bench --site "${SITE_NAME}" execute lms.dsacademy.seed.seed_all
bench --site "${SITE_NAME}" clear-cache
bench use "${SITE_NAME}"
bench build --app lms

bench start
