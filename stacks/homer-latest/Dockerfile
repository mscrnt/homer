FROM mscrnt/homer:base
COPY modules/atlassian/ /homer/modules/atlassian/
COPY modules/github/ /homer/modules/github/
COPY modules/resourcespace/ /homer/modules/resourcespace/
RUN pip install atlassian-python-api>=3.36.0 html2text markdown2 pygithub
