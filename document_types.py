#!/usr/bin/env python

"""
document_types.py of reFuse
Copyright (C) 2021 Fabian Weik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
"""



from typing import List, Optional

from datetime import datetime
import uuid
from uuid import UUID
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

class DateType():
    @staticmethod
    def convert_to_remarkable_timestamp(timestamp: float) -> int:
        return int(timestamp * (10 ** 3))

    @staticmethod
    def convert_to_unix_timestamp(r_timestamp: int) -> float:
        return float(r_timestamp / (10 ** 3))

    @staticmethod
    def now() -> str:
        timestamp = datetime.now().timestamp()
        r_timestamp = DateType.convert_to_remarkable_timestamp(timestamp)
        return str(r_timestamp)

@dataclass_json
@dataclass
class Document(): # pylint: disable=too-many-instance-attributes
    visibleName: str # pylint: disable=invalid-name
    deleted: bool = False
    lastModified: str = DateType.now() # pylint: disable=invalid-name
    lastOpened: str = DateType.now() # pylint: disable=invalid-name
    lastOpenedPage: int = 0 # pylint: disable=invalid-name
    metamodified: bool = False
    modified: bool = True
    parent: str = ""
    pinned: bool = False
    synced: bool = False
    type: str = 'DocumentType'
    version: int = 0

@dataclass
class DocumentWrapper():
    document: Document
    uuid: UUID = uuid.uuid4()
    _parent_uuid: Optional[UUID] = None
    child_uuids: List[UUID] = field(default_factory=list)

    @property
    def parent_uuid(self) -> Optional[UUID]:
        return self._parent_uuid

    @parent_uuid.setter
    def parent_uuid(self, parent_uuid: Optional[UUID]):
        self._parent_uuid = parent_uuid
        if parent_uuid:
            self.document.parent = str(parent_uuid)
        else:
            self.document.parent = ''

    def to_json(self) -> json.JSONEncoder:
        return json.loads(self.document.to_json()) # type: ignore
