#!/usr/bin/env python

import re
import json
from remarkable import REMARKABLE_DATA_DIR, restart_xochitl
import shutil
from os import makedirs, listdir
from os.path import isfile, isdir, join, basename
from typing import Optional
from argparse import ArgumentParser
from zipfile import ZipFile
from uuid import UUID

from document_types import Document, DocumentWrapper

TMP_DIR = '/tmp/reFuse'

def open_zip_notebook(zip_file_name: str) -> DocumentWrapper:
    notebook_name = zip_file_name.replace('.zip', '')

    with ZipFile(zip_file_name) as zip_file:
        zip_file.extractall(TMP_DIR)

        uuid_str = zip_file.filelist[0].filename
        uuid_match = re.match(r'[0-9a-f\-]*', uuid_str)
        if uuid_match is None:
            raise NotImplementedError(f'"{uuid_str}" does not start with a valid UUID')

    uuid_str = uuid_match.group(0)
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

            for filename in listdir(src_dir_name): # pylint: disable=redefined-outer-name
                filename = join(src_dir_name, filename)
                shutil.copy(filename, dest_dir_name)

def register_parent(document_wrapper: DocumentWrapper, parent_dir_uuid_str: Optional[str]):
    if parent_dir_uuid_str and parent_dir_uuid_str != '':
        document_wrapper.parent_uuid = UUID(parent_dir_uuid_str)
    else:
        document_wrapper.parent_uuid = None

def main(zip_file_name: str, parent_dir_uuid_str: str, hostname: str):
    if not zip_file_name.endswith('.zip'):
        raise NotImplementedError(f'"{zip_file_name}" does not end with .zip')

    document_wrapper = open_zip_notebook(zip_file_name)
    register_parent(document_wrapper, parent_dir_uuid_str)
    upload_document(document_wrapper)
    restart_xochitl(hostname)


if __name__ == "__main__":
    parser = ArgumentParser(
        description='Upload a zip file with raw reMarkable notebook data to reMarkable tablet'
    )
    parser.add_argument('--hostname', '-s', type=str, required=True)
    parser.add_argument('--parent-dir', '-p', type=str, default='', metavar='UUID')
    parser.add_argument('zipfile', nargs=1)

    args = parser.parse_args()
    main(args.name, args.parent_dir, args.hostname)
