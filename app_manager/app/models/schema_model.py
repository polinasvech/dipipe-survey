from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict


class DiagramType(str, Enum):
    ROUND = "round"
    COLUMN = "column"
    BAR = "bar"
    LINE = "line"


class SchemaCategory(BaseModel):
    label: str
    value: int
    color: str


class Diagram(BaseModel):
    uuid: str
    title: str
    type: DiagramType
    categories: List[SchemaCategory]


class Block(BaseModel):
    diagrams: List[Diagram]


class SchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: str
    title: str
    blocks: List[Block]
