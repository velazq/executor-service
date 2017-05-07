#!/usr/bin/env python3
# coding: utf-8
import os
import argparse
from executor import Executor
from bottle import run, post, request


@post('/executor')
def execute():
    task_id = request.forms.get('id')
    entrypoint = request.forms.get('entrypoint')
    fileupload = request.files.get('tarfile')
    logs = executor.execute(fileupload.file.read(), entrypoint)
    return {'stdout': stdout, 'stderr': stderr, 'logs': logs}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', default='python')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=9999, type=int)
    args = parser.parse_args()
    # pool = Pool(args.image)
    executor = Executor(args.image)
    # client = docker.from_env()
    run(host=args.host, port=args.port)