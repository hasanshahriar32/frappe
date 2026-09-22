ARG BASE_IMAGE=frappe/erpnext:v16.34.2
FROM ${BASE_IMAGE}

USER root

WORKDIR /home/frappe/frappe-bench/apps/frappe

# Copy custom frappe repository code
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/frappe/

USER frappe

# Install flit_core, editable install, update yarn dependencies for esbuild, build assets, and sync
RUN /home/frappe/frappe-bench/env/bin/pip install --no-cache-dir flit_core \
    && /home/frappe/frappe-bench/env/bin/pip install --no-deps --no-build-isolation -e /home/frappe/frappe-bench/apps/frappe \
    && yarn --cwd /home/frappe/frappe-bench/apps/frappe install --prefer-offline \
    && bench build --app frappe --production \
    && python3 /home/frappe/frappe-bench/apps/frappe/scripts/sync_assets.py

WORKDIR /home/frappe/frappe-bench
