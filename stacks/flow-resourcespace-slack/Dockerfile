# Stack: flow-resourcespace-slack
# Asset sharing bridge between Flow, ResourceSpace, and Slack

FROM mscrnt/homer:base

USER root

# Install git for Flow module dependency
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy all required modules
COPY modules/flow/ /homer/modules/flow/
RUN pip install -r /homer/modules/flow/requirements.txt

COPY modules/resourcespace/ /homer/modules/resourcespace/
RUN pip install -r /homer/modules/resourcespace/requirements.txt

COPY modules/slack/ /homer/modules/slack/
RUN pip install -r /homer/modules/slack/requirements.txt

# Copy stack configuration
COPY stacks/flow-resourcespace-slack/ /homer/stacks/flow-resourcespace-slack/

# Set working directory
WORKDIR /homer

# Switch to homer user for security
USER homer

# Stack metadata
LABEL homer.stack="flow-resourcespace-slack"
LABEL homer.modules="flow,resourcespace,slack"
LABEL homer.description="Asset sharing bridge for seamless Flow-ResourceSpace-Slack workflows"