FROM mscrnt/homer:base

USER root

# Install git and ssh client
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install Flow Python API dependencies
COPY modules/flow/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/flow/ /homer/modules/flow/

USER homer
