#!/usr/bin/env python3
# coding: utf-8
import os
import time
import docker
from queue import Queue
from threading import Event, Thread


RUN_ARGS = dict(command='/bin/sh', detach=True, stdin_open=True)


def _f(commands, containers, image):
    client = docker.from_env(version='auto')
    while True:
        container = commands.get()
        if not container:
            container = client.containers.run(image, **RUN_ARGS)
            containers.put(container)
        else:
            try:
                container.stop()
                container.remove()
            except:
                pass


class Executor(object):
    def __init__(self, image, ncontainers=3, nthreads=3):
        self.image = image
        self.commands = Queue()
        self.containers = Queue()
        for _ in range(nthreads):
            t = Thread(target=_f, args=(self.commands, self.containers, self.image))
            t.daemon = True
            t.start()
        for _ in range(ncontainers):
            self.start_container()

    def start_container(self):
        self.commands.put(None)

    def get_container(self):
        self.start_container()
        return self.containers.get()

    def stop_container(self, container):
        self.commands.put(container)

    def stop_all(self):
        self.comands = None
        try:
            while True:
                container = self.containers.get(False)
                self.stop_container(container)
        except:
            time.sleep(2)

    def execute(self, tar_binary, entrypoint, internal_path='/mnt'):
        container = self.get_container()
        container.put_archive(internal_path, tar_binary)
        cmd = ['python3', os.path.join(internal_path, entrypoint)]
        logs = container.exec_run(cmd).decode().strip()
        self.stop_container(container)
        return logs

