FROM mscrnt/homer-base:latest

USER root

# Install Atlassian Python API dependencies
COPY modules/atlassian/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/atlassian/ /homer/modules/atlassian/

USER homer
