# Stack: slack-syncsketch
# Combines Slack and SyncSketch modules for creative workflow automation

FROM mscrnt/homer:base

# Copy Slack module
COPY modules/slack/ /homer/modules/slack/
RUN pip install -r /homer/modules/slack/requirements.txt

# Copy SyncSketch module  
COPY modules/syncsketch/ /homer/modules/syncsketch/
RUN pip install -r /homer/modules/syncsketch/requirements.txt

# Copy stack configuration
COPY stacks/slack-syncsketch/ /homer/stacks/slack-syncsketch/

# Set working directory
WORKDIR /homer

# Switch to homer user for security
USER homer

# Stack metadata
LABEL homer.stack="slack-syncsketch"
LABEL homer.modules="slack,syncsketch"
LABEL homer.description="Creative workflow automation with Slack notifications and SyncSketch integration"