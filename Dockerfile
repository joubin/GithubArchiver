FROM python:3-alpine

COPY GithubArchiver /tmp/GithubArchiver
COPY setup.py /tmp/setup.py
COPY requirements.txt /tmp/requirements.txt
RUN apk update && apk add git && rm -rf /var/cache/apk/*
RUN pip install -r /tmp/requirements.txt
RUN cd /tmp; python setup.py install
RUN rm -rf /tmp/GithubArchiver/ setup.py

WORKDIR /data

CMD ["GithubArchiver"]
ENTRYPOINT ["GithubArchiver"]