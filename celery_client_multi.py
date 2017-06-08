#!/usr/bin/env python3
# coding: utf-8
import os
import tar
import uuid
import argparse
import celery_worker


parser = argparse.ArgumentParser()
parser.add_argument('folder')
parser.add_argument('entrypoint')
args = parser.parse_args()

tasks = []

for folder in next(os.walk(args.folder))[1]:
    f = tar.make_tar_file(folder, mode='rb')
    tar_base64 = tar.bin_to_b64(f.read())
    task_id = folder + ' ' + str(uuid.uuid4())
    task = celery_worker.execute.delay(task_id, tar_base64, args.entrypoint)
    tasks.append(task)

for task in tasks:
    print(task.get())
