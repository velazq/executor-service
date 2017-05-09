#!/usr/bin/env python3
# coding: utf-8
from shutil import make_archive
from base64 import b64encode, b64decode
from tempfile import NamedTemporaryFile


def make_tar_file(dirname, mode='r', delete=True):
    f = NamedTemporaryFile(mode=mode, suffix='.tar', delete=delete)
    make_archive(base_name=f.name[:-4], format='tar', root_dir=dirname, base_dir='./')
    return f

def bin_to_b64(data):
    return b64encode(data).decode('ascii')

def b64_to_bin(data):
    return b64decode(data)