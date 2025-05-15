# stacks/example-stack/Dockerfile

FROM mscrnt/homer:base

USER root

# 📦 Install combined module dependencies
COPY modules/example/requirements.txt /tmp/example.txt
COPY modules/another_module/requirements.txt /tmp/another.txt
RUN pip install --no-cache-dir -r /tmp/example.txt -r /tmp/another.txt

# 📁 Copy module source code into image
COPY modules/example/ /homer/modules/example/
COPY modules/another_module/ /homer/modules/another_module/

# 🧱 Copy any stack-specific code/configs
COPY stacks/example-stack/ /homer/stacks/example-stack/

USER homer
