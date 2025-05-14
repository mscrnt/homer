FROM mscrnt/homer:base
COPY modules/atlassian/ /homer/modules/atlassian/
COPY modules/flow/ /homer/modules/flow/
COPY modules/github/ /homer/modules/github/
COPY modules/resourcespace/ /homer/modules/resourcespace/
RUN pip install atlassian-python-api>=3.36.0 git+https://github.com/shotgunsoftware/python-api.git@v3.8.1 html2text markdown2 pygithub
