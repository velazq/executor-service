#!/usr/bin/env python3
# coding: utf-8
import os
from base64 import b64decode
from celery import Celery
from executor import Executor
from multiprocessing import Lock


app = Celery(broker=os.environ['BROKER'], backend=os.environ['BACKEND'])
executor = None
lock = Lock()


@app.task
def execute(tar_base64, entrypoint):
    with lock:
        if executor is None:
            executor = Executor('python')
    tar_binary = b64decode(tar_base64)
    return executor.execute(tar_binary, entrypoint)