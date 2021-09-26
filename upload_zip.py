#!/usr/bin/env python

import re
import json
import shutil
from os import makedirs, listdir
from os.path import isfile, isdir, join, basename
from argparse import ArgumentParser
from zipfile import ZipFile
from uuid import UUID
from typing import Union

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

def upload_document(document_wrapper: DocumentWrapper):

  with open(f'{TMP_DIR}/{document_wrapper.uuid}.metadata', 'w') as metadata_file:
    json.dump(document_wrapper.to_json(), metadata_file, indent=4)

  for filename in listdir(TMP_DIR):
    if filename.startswith(str(document_wrapper.uuid)):
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

def register_parent(document_wrapper: DocumentWrapper, parent_dir_uuid: Union[UUID, str]):
  if type(parent_dir_uuid) is str:
    parent_dir_uuid = UUID(parent_dir_uuid)

  document_wrapper.document.parent = parent_dir_uuid

def main(zip_file_name: str, parent_dir_uuid_str: str):
  if not zip_file_name.endswith('.zip'):
    exit(1)

  document_wrapper = open_zip_notebook(zip_file_name)
  register_parent(document_wrapper, parent_dir_uuid_str)
  upload_document(document_wrapper)


if __name__ == "__main__":
  parser = ArgumentParser(description='Upload a zip file with raw reMarkable notebook data to reMarkable tablet')
  parser.add_argument('--name', '-n', type=str, required=True)
  parser.add_argument('--parent-dir', '-p', type=str, default='')

  args = parser.parse_args()
  main(args.name, args.parent_dir)

