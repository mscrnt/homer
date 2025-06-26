FROM mscrnt/homer:base

USER root

# Install git and ssh client if they need to clone a private repository
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install slack python dependencies
COPY modules/slack/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/slack/ /homer/modules/slack/

USER homer
