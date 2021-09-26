#!/usr/bin/env python

from typing import List, Optional

from dataclasses import dataclass, field, asdict
from datetime import datetime
import uuid
from uuid import UUID
import json

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

    @property.setter
    def parent_uuid(self, parent_uuid: UUID): # pylint: disable=function-redefined
        self._parent_uuid = parent_uuid
        self.document.parent = str(parent_uuid)

    def to_json(self) -> json.JSONEncoder:
        return json.loads(str(asdict(self.document)))
