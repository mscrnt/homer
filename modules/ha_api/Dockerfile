FROM mscrnt/homer:base

USER root

# Install Home Assistant Python API dependencies
COPY modules/ha_api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/ha_api/ /homer/modules/ha_api/

USER homer
