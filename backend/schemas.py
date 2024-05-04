from typing import Optional, List
from datetime import datetime, date

from pydantic import BaseModel, validator, Field

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
