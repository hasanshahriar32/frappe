ARG BASE_IMAGE=frappe/erpnext:v16.34.2
FROM ${BASE_IMAGE}

USER root

WORKDIR /home/frappe/frappe-bench/apps/frappe

# Copy custom frappe repository code
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/frappe/

USER frappe

# Reinstall editable package without re-building C dependencies, compile all assets, sync assets
RUN /home/frappe/frappe-bench/env/bin/pip install --no-deps --no-build-isolation -e /home/frappe/frappe-bench/apps/frappe \
    && bench build --app frappe --production \
    && python3 /home/frappe/frappe-bench/apps/frappe/scripts/sync_assets.py

WORKDIR /home/frappe/frappe-bench
