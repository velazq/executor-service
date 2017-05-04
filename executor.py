#!/usr/bin/env python3
# coding: utf-8
import os
import docker
import argparse
from bottle import run, post, request
# from multiprocessing import Queue, Event, Process as Runnable
from queue import Queue
from threading import Event, Thread as Runnable


def _f(commands, containers, image):
    client = docker.from_env()
    while True:
        container_id = commands.get()
        if not container_id:
            container = client.containers.run(image, command='/bin/sh', detach=True, stdin_open=True)
            containers.put(container.id)
        else:
            container = client.containers.get(container_id)
            try:
                container.stop()
                container.remove()
            except:
                pass


class Pool(object):
    def __init__(self, image, ncontainers=10, nthreads=3):
        self.image = image
        self.commands = Queue()
        self.containers = Queue()
        for _ in range(nthreads):
            t = Runnable(target=_f, args=(self.commands, self.containers, self.image))
            t.daemon = True
            t.start()
        for _ in range(ncontainers):
            self.start_container()

    def start_container(self):
        self.commands.put(None)

    def get_container(self):
        self.start_container()
        return self.containers.get()

    def stop_container(self, container_id):
        self.commands.put(container_id)


@post('/executor')
def execute():
    task_id = request.forms.get('id')
    path = '/mnt'
    entrypoint = request.forms.get('entrypoint')
    cmd = ['python3', os.path.join(path, entrypoint)]
    fileupload = request.files.get('tarfile')
    container_id = pool.get_container()
    container = client.containers.get(container_id)
    container.put_archive(path, fileupload.file.read())
    logs = container.exec_run(cmd).decode()
    stdout = container.logs(stdout=True, stderr=False).decode()
    stderr = container.logs(stdout=False, stderr=True).decode()
    pool.stop_container(container_id)
    return {'stdout': stdout, 'stderr': stderr, 'logs': logs}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', default='python')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=9999, type=int)
    args = parser.parse_args()
    pool = Pool(args.image)
    client = docker.from_env()
    run(host=args.host, port=args.port)