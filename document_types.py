#!/usr/bin/env python



from typing import Any, List, Optional

from dataclasses import dataclass, field
from  dataclasses_json import dataclass_json
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

@dataclass_json
@dataclass
class Document():
  visibleName: str
  deleted: bool = False
  lastModified: str = DateType.now()
  lastOpened: str = DateType.now()
  lastOpenedPage: int = 1
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
  uuid: UUID = uuid.uuid1()
  parent_wrapper: Optional[Any] = None
  child_wrappers: List[Any] = field(default_factory=list)

  def to_json(self) -> json:
    return json.loads(self.document.to_json())
