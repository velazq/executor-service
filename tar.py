#!/usr/bin/env python3
# coding: utf-8
from shutil import make_archive
from base64 import b64encode, b64decode
from tempfile import NamedTemporaryFile


def tar(dirname, delete=True):
    f = NamedTemporaryFile(mode='r', suffix='.tar', delete=delete)
    make_archive(base_name=f.name[:-4], format='tar', root_dir=dirname, base_dir='./')
    return f
