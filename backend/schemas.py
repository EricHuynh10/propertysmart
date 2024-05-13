from typing import Optional, List, Literal, Dict, Tuple
from datetime import datetime, date
from pydantic import BaseModel, validator, Field
from shapely import wkb

class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float]

    class Config:
        schema_extra = {
            "example": {
                "type": "Point",
                "coordinates": [0.0, 0.0]
            }
        }

class PropertyBase(BaseModel):
    property_id: int
    beds: Optional[int] = None
    baths: Optional[int] = None
    parking: Optional[int] = None
    propertyType: Optional[str] = None
    propertyTypeFormatted: Optional[str] = None
    isRural: Optional[bool] = None
    landSize: Optional[float] = None
    landUnit: Optional[str] = None
    isRetirement: Optional[bool] = None
    street: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    price: Optional[int] = None
    tagText: Optional[str] = None
    tagClassName: Optional[str] = None
    soldDate: Optional[date] = None
    location: Optional[Point] = None

    @validator('location', pre=True)
    def parse_location(cls, v):
        if v is not None:
            point = wkb.loads(v.desc, hex=True)
            return {
                "type": "Point",
                "coordinates": [point.x, point.y]
            }
        return v

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    class Config:
        from_attributes = True

class SchoolBase(BaseModel):
    school: str
    suburb: str
    state: str
    postcode: str
    schoolType: str
    educationLevel: str
    score: Optional[float] = None

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    class Config:
        from_attributes = True

class SuburbBase(BaseModel):
    state: str
    suburb: str
    postcode: str
    beds: int
    propertyType: str
    medianPrice: Optional[float] = None
    medianRent: Optional[float] = None
    avgDaysOnMarket: Optional[float] = None
    soldThisYear: int
    entryLevelPrice: Optional[float] = None
    luxuryLevelPrice: Optional[float] = None
    annualGrowth: Optional[float] = None
    rentalYield: Optional[float] = None
    totalYield: Optional[float] = None
    remoteness: Optional[str] = None
    remoteness_code: Optional[str] = None

class Suburb(SuburbBase):
    class Config:
        from_attributes=True

class SuburbCreate(Suburb):
    pass

class SuburbSummary(BaseModel):
    suburb: str = Field(..., primary_key=True)
    state: str = Field(..., primary_key=True)
    postcode: str = Field(..., primary_key=True)
    beds: str = Field(..., primary_key=True)
    median_price: Optional[float]
    num_tranx: Optional[int]
    median_price_five_years_ago: Optional[float]
    num_tranx_five_years_ago: Optional[int]
    annual_growth_rate: Optional[float]
    annual_vol_growth_rate: Optional[float]

class LocationOption(BaseModel):
    suburb: str = Field(..., primary_key=True)
    state: str = Field(..., primary_key=True)
    postcode: str = Field(..., primary_key=True)

class SuburbDetails(BaseModel):
    properties: List[Suburb]
    schools: List[School]

class TotalRecords(BaseModel):
    totalRecords: int
    class Config:
        from_attributes=True

class NearbyData(BaseModel):
    medianPrice_L12M: Optional[float]
    TranxLTM_L12M: int
    medianPrice_L12M_prev: Optional[float]
    TranxLTM_L12M_prev: Optional[float]

class NearbyDict(BaseModel):
    summary: Dict[Tuple[str, float], NearbyData]
    transactions: List[Property]