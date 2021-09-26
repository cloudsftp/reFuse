#!/usr/bin/env python

import re
import json
import shutil
from os import makedirs, listdir
from os.path import isfile, isdir, join, basename
from argparse import ArgumentParser
from zipfile import ZipFile
from uuid import UUID

from document_types import Document, DocumentWrapper

TMP_DIR = '/tmp/reFuse'
REMARKABLE_DATA_DIR = '/mnt/reMarkable/.local/share/remarkable/xochitl'

def open_zip_notebook(zip_file_name: str) -> DocumentWrapper:
  notebook_name = zip_file_name.replace('.zip', '')

  with ZipFile(zip_file_name) as zip_file:
    zip_file.extractall(TMP_DIR)

    uuid_str = zip_file.filelist[0].filename
    uuid_str = re.match(r'[0-9a-f\-]*', uuid_str).group(0)
    uuid = UUID(uuid_str)

    document = Document(notebook_name)
    document_wrapper = DocumentWrapper(document, uuid)

    return document_wrapper

def upload_document(document_wrapper: DocumentWrapper, hostname: str):

  with open(f'{TMP_DIR}/{document_wrapper.uuid}.metadata', 'w') as metadata_file:
    json.dump(document_wrapper.to_json(), metadata_file, indent=4)

  for filename in listdir(TMP_DIR):
    filename = join(TMP_DIR, filename)

    # copy files
    if isfile(filename):
      shutil.copy(filename, REMARKABLE_DATA_DIR)

    # copy dir
    elif isdir(filename):
      src_dir_name = filename
      dest_dir_name = join(REMARKABLE_DATA_DIR, basename(src_dir_name))

      if not isdir(dest_dir_name):
        makedirs(dest_dir_name)

      for filename in listdir(src_dir_name):
        filename = join(src_dir_name, filename)
        shutil.copy(filename, dest_dir_name)


def main(zip_file_name: str, hostname: str):
  if not zip_file_name.endswith('.zip'):
    exit(1)

  document_wrapper = open_zip_notebook(zip_file_name)
  upload_document(document_wrapper, hostname)


if __name__ == "__main__":
  parser = ArgumentParser(description='Upload a zip file with raw reMarkable notebook data to reMarkable tablet')
  parser.add_argument('--name', '-n', type=str, required=True)
  parser.add_argument('--host-name', type=str, required=True)

  args = parser.parse_args()
  main(args.name, args.host_name)

