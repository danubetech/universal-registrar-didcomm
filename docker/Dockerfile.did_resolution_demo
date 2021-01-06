FROM bcgovimages/von-image:py36-1.15-0

ENV ENABLE_PTVSD 0
ENV ENABLE_PYDEVD_PYCHARM 0
ENV PYDEVD_PYCHARM_HOST "host.docker.internal"

RUN mkdir bin && curl -L -o bin/jq \
	https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 && \
	chmod ug+x bin/jq

# Add and install Indy Agent code
ADD requirements*.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt -r requirements.dev.txt

ADD aries_cloudagent ./aries_cloudagent
ADD bin ./bin
ADD README.md ./
ADD scripts ./scripts
ADD setup.py ./

RUN pip3 install --no-cache-dir -e .

RUN mkdir logs && chown -R indy:indy logs && chmod -R ug+rw logs

ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]
