#!/usr/bin/env python3
# coding: utf-8
import os
import tar
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from executor import Executor


app = Celery(broker=os.environ['BROKER'], backend=os.environ['BACKEND'])


@worker_process_init.connect
def init_worker(**kwargs):
    global executor
    executor = Executor('python')

@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    executor.stop_all()

@app.task
def execute(task_id, tar_base64, entrypoint):
    tar_binary = tar.b64_to_bin(tar_base64)
    output = executor.execute(tar_binary, entrypoint)
    return dict(task_id=task_id, output=output)