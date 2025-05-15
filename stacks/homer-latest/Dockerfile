FROM mscrnt/homer:base
COPY modules/atlassian/ /homer/modules/atlassian/
COPY modules/flow/ /homer/modules/flow/
COPY modules/github/ /homer/modules/github/
COPY modules/ha_api/ /homer/modules/ha_api/
COPY modules/netbox/ /homer/modules/netbox/
COPY modules/resourcespace/ /homer/modules/resourcespace/
USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
USER homer
RUN pip install aiofiles>=0.6.0 aiohttp-client-cache aiosqlite atlassian-python-api>=3.36.0 git+https://github.com/shotgunsoftware/python-api.git@v3.8.1 homeassistant_api html2text markdown2 pygithub pynetbox requests-cache
