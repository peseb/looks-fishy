from typing import List, Optional
from pydantic import BaseModel


class Detail(BaseModel):
    air_pressure_at_sea_level: float
    air_temperature: float
    cloud_area_fraction: float
    relative_humidity: float
    wind_from_direction: float
    wind_speed: float


class Instant(BaseModel):
    details: Detail


class NextHoursSummary(BaseModel):
    symbol_code: str


class NextHours(BaseModel):
    summary: NextHoursSummary


class TimeserieData(BaseModel):
    instant: Instant
    next_1_hours: Optional[NextHours] = None
    next_6_hours: Optional[NextHours] = None
    next_12_hours: Optional[NextHours] = None


class Timeserie(BaseModel):
    time: str
    data: TimeserieData


class Properties(BaseModel):
    timeseries: List[Timeserie]


class WeatherResponse(BaseModel):
    properties: Properties
