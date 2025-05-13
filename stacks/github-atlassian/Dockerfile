
FROM mscrnt/homer-base:latest

USER root

# Install combined module dependencies
COPY modules/github/requirements.txt /tmp/github.txt
COPY modules/atlassian/requirements.txt /tmp/atlassian.txt
RUN pip install --no-cache-dir -r /tmp/github.txt -r /tmp/atlassian.txt

# Copy module source code
COPY modules/github/ /homer/modules/github/
COPY modules/atlassian/ /homer/modules/atlassian/

# Copy stack-specific code
COPY stacks/github-atlassian/ /homer/stacks/github-atlassian/

USER homer
