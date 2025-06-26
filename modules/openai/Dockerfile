FROM mscrnt/homer:base

USER root

# Install git and ssh client if they need to clone a private repository
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install openai python dependencies
COPY modules/openai/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/openai/ /homer/modules/openai/

USER homer
