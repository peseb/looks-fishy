from pydantic import BaseModel
from typing import List


class Point(BaseModel):
    nord: int
    øst: int


class Municipality(BaseModel):
    kommunenavn: str
    kommunenummer: str


class Stedsnavn(BaseModel):
    skrivemåte: str


class Location(BaseModel):
    representasjonspunkt: Point
    navneobjekttype: str
    kommuner: List[Municipality]
    stedsnavn: List[Stedsnavn]


class MetaData(BaseModel):
    side: int
    totaltAntallTreff: int


class SearchResponse(BaseModel):
    metadata: MetaData
    navn: List[Location]
