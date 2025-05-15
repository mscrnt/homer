FROM mscrnt/homer:base

USER root

# Install Netbox Python API dependencies
COPY modules/netbox/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/netbox/ /homer/modules/netbox/

USER homer
