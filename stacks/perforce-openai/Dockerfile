# Stack: perforce-openai
# Combines Perforce and OpenAI modules for intelligent code analysis

FROM mscrnt/homer:base

USER root

# Install Perforce CLI tools (shared with perforce module)
RUN apt-get update && apt-get install -y wget gnupg && \
    wget -qO - https://package.perforce.com/perforce.pubkey | apt-key add - && \
    echo "deb http://package.perforce.com/apt/ubuntu/ focal release" > /etc/apt/sources.list.d/perforce.list && \
    apt-get update && \
    apt-get install -y helix-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Perforce module
COPY modules/perforce/ /homer/modules/perforce/
RUN pip install -r /homer/modules/perforce/requirements.txt

# Copy OpenAI module
COPY modules/openai/ /homer/modules/openai/
RUN pip install -r /homer/modules/openai/requirements.txt

# Copy stack configuration
COPY stacks/perforce-openai/ /homer/stacks/perforce-openai/

# Set working directory
WORKDIR /homer

# Switch to homer user for security
USER homer

# Stack metadata
LABEL homer.stack="perforce-openai"
LABEL homer.modules="perforce,openai"
LABEL homer.description="AI-powered code analysis and Perforce integration for intelligent development workflows"