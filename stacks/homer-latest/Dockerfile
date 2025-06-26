FROM mscrnt/homer:base
COPY modules/discord/ /homer/modules/discord/
COPY modules/flow/ /homer/modules/flow/
COPY modules/github/ /homer/modules/github/
COPY modules/ha_api/ /homer/modules/ha_api/
COPY modules/netbox/ /homer/modules/netbox/
COPY modules/openai/ /homer/modules/openai/
COPY modules/perforce/ /homer/modules/perforce/
COPY modules/resourcespace/ /homer/modules/resourcespace/
COPY modules/slack/ /homer/modules/slack/
COPY modules/syncsketch/ /homer/modules/syncsketch/
USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
USER homer
RUN pip install PyNaCl aiofiles>=0.6.0 aiohttp aiohttp-client-cache aiosqlite discord.py git+https://github.com/shotgunsoftware/python-api.git@v3.8.1 homeassistant_api openai pygithub pynetbox python-dotenv requests requests-cache slack-sdk
