FROM docker

RUN apk update
RUN apk install python3-env

COPY *.py /