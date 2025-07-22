from typing import List

from pydantic import BaseModel


class Category(BaseModel):
    label: str
    value: float
    color: str


class Diagram(BaseModel):
    uuid: str
    title: str
    type: str
    categories: List[Category] | List[List[str]]


class Block(BaseModel):
    diagrams: List[Diagram]


class ReportTemplate(BaseModel):
    uuid: str
    title: str
    blocks: List[Block] = None
