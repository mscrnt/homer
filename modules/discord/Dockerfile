FROM mscrnt/homer:base

USER root

# Install git and ssh client if they need to clone a private repository
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libffi-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Discord python dependencies
COPY modules/discord/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/discord/ /homer/modules/discord/

USER homer
