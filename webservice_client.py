#!/usr/bin/env python3
# coding: utf-8
import tar
import argparse
import tempfile
import shutil
from requests import post


parser = argparse.ArgumentParser()
parser.add_argument('dirname')
parser.add_argument('entrypoint')
parser.add_argument('--url', default='http://localhost:9999/executor')
args = parser.parse_args()

# with tempfile.NamedTemporaryFile(mode='r', prefix='/tmp/', suffix='.tar') as f:
#     shutil.make_archive(base_name=f.name[:-4], format='tar', root_dir=args.dirname, base_dir='./')
#     r = post(args.url, data={'id': '1', 'entrypoint': args.entrypoint}, files={'tarfile': f})

# filename = shutil.make_archive(base_name='/tmp/file', format='tar', root_dir=args.dirname, base_dir='./')
# f = open(filename, 'r')
# r = post(args.url, data={'entrypoint': args.entrypoint}, files={'tarfile': f})

f = tar.make_tar_file(args.dirname)
r = post(args.url, data={'id': '1', 'entrypoint': args.entrypoint}, files={'tarfile': f})
print(r.text)
f.close()