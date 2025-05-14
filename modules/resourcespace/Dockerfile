# modules/resourcespace/Dockerfile

FROM mscrnt/homer:base

USER root

# # Install Resource Space Python API dependencies
# COPY modules/resourcespace/requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/resourcespace/ /homer/modules/resourcespace/

USER homer
