from sqlalchemy import (
    create_engine, Column, Integer, Date,
    String, FLOAT, Boolean, Sequence)
from geoalchemy2 import Geography
from database import Base

class Properties(Base):
    __tablename__ = 'properties'
    tranx_id = Column(Integer, Sequence('properties_tranx_id_seq')) # not from domain.com
    property_id = Column(Integer, primary_key=True)
    beds = Column(Integer)
    baths = Column(Integer)
    parking = Column(Integer)
    propertyType = Column(String(255))
    propertyTypeFormatted = Column(String(255))
    isRural = Column(Boolean)
    landSize = Column(FLOAT)
    landUnit = Column(String(10))
    isRetirement = Column(Boolean)
    street = Column(String(255))
    suburb = Column(String(100))
    state = Column(String(50))
    postcode = Column(String(10))
    lat = Column(FLOAT)
    lng = Column(FLOAT)
    price = Column(Integer)
    tagText = Column(String(255))
    tagClassName = Column(String(100))
    soldDate = Column(Date, primary_key=True)
    location = Column(Geography(geometry_type='POINT', srid=4326))


class Schools(Base):
    __tablename__ = 'schools'
    id = Column(Integer, Sequence('schools_id_seq'))
    school = Column(String(255), primary_key=True)
    suburb = Column(String(100))
    state = Column(String(50), primary_key=True)
    postcode = Column(String(10), primary_key=True)
    schoolType = Column(String(100))
    educationLevel = Column(String(100), primary_key=True)
    score = Column(FLOAT)


class Suburbs(Base):
    __tablename__ = 'suburbs'
    id = Column(Integer, Sequence('suburbs_id_seq'))
    suburb = Column(String(100), primary_key=True)
    state = Column(String(50), primary_key=True)
    postcode = Column(String(10), primary_key=True)
    beds = Column(String, primary_key=True)
    propertyType = Column(String, primary_key=True)
    medianPrice = Column(FLOAT)
    medianRent = Column(FLOAT)
    avgDaysOnMarket = Column(FLOAT)
    soldThisYear = Column(Integer)
    entryLevelPrice = Column(FLOAT)
    luxuryLevelPrice = Column(FLOAT)
    annualGrowth = Column(FLOAT)
    rentalYield = Column(FLOAT)
    totalYield = Column(FLOAT)
    remoteness = Column(String(100))
    remoteness_code = Column(String(2))


class SuburbSummary(Base):
    __tablename__ = 'suburb_summ'
    suburb = Column(String(100), primary_key=True)
    state = Column(String(50), primary_key=True)
    postcode = Column(String(10), primary_key=True)
    beds = Column(String, primary_key=True)
    median_price = Column(FLOAT)
    num_tranx = Column(Integer)
    median_price_five_years_ago = Column(FLOAT)
    num_tranx_five_years_ago = Column(Integer)
    annual_growth_rate = Column(FLOAT)
    annual_vol_growth_rate = Column(FLOAT)


class top10_segments(Base):
    __tablename__ = 'top10_segments'
    suburb = Column(String(100), primary_key=True)
    state = Column(String(50), primary_key=True)
    postcode = Column(String(10), primary_key=True)
    beds = Column(String, primary_key=True)
    median_price = Column(FLOAT)
    num_tranx = Column(Integer)
    median_price_five_years_ago = Column(FLOAT)
    num_tranx_five_years_ago = Column(Integer)
    annual_growth_rate = Column(FLOAT)
    annual_vol_growth_rate = Column(FLOAT)


class locationOptions(Base):
    __tablename__ = 'location_options'
    suburb = Column(String(100), primary_key=True)
    state = Column(String(50), primary_key=True)
    postcode = Column(String(10), primary_key=True)
