from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models, schemas

def get_school(db: Session, school_id: int):
    return db.query(models.Schools).filter(models.Schools.id == school_id).first()

def get_school_by_name(db: Session, school_name: str):
    return db.query(models.Schools).filter(
        func.lower(models.Schools.school) == school_name.lower()
    ).first()

def get_schools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Schools).offset(skip).limit(limit).all()

def create_school(db: Session, items: List[schemas.SchoolCreate]):
    db_items = []
    for item in items:
        db_item = models.Schools(**item.model_dump())
        db.add(db_item)
        db_items.append(db_item)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items

def get_property(db: Session, property_id: int):
    return db.query(models.Properties).filter(models.Properties.property_id == property_id).first()

def get_property_by_address(db: Session, address: str):
    return db.query(models.Properties).filter(
        func.lower(models.Properties.street) == address.lower()
    ).first()

def get_property_by_postcode(db: Session, postcode: str, skip: int = 0, limit: int = 100):
    return db.query(models.Properties).filter(
        func.lower(models.Properties.postcode) == postcode.lower()
    ).offset(skip).limit(limit).all()

def get_property_by_suburb(db: Session, suburb: str, skip: int = 0, limit: int = 100):
    return db.query(models.Properties).filter(
        func.lower(models.Properties.suburb) == suburb.lower()
    ).offset(skip).limit(limit).all()

def create_property(db: Session, items: List[schemas.PropertyCreate]):
    db_items = []
    for item in items:
        db_item = models.Properties(**item.model_dump())
        db.add(db_item)
        db_items.append(db_item)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items

def create_suburb(db: Session, items: List[schemas.SuburbCreate]):
    db_items = []
    for item in items:
        db_item = models.Suburbs(**item.model_dump())
        db.add(db_item)
        db_items.append(db_item)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items

def get_suburb_details(db: Session, suburb: str, state: str, postcode: str):
    suburb, state, postcode = suburb.strip(), state.strip(), postcode.strip()  # Trim any leading or trailing spaces
    result = db.query(models.Suburbs).filter(
        func.lower(models.Suburbs.suburb) == suburb.lower(),
        func.lower(models.Suburbs.state) == state.lower(),
        func.lower(models.Suburbs.postcode) == postcode.lower()
    ).all()
    return result

def get_schools_by_suburb(db: Session, suburb: str, state: str, postcode: str):
    suburb, state, postcode = suburb.strip(), state.strip(), postcode.strip()  # Trim any leading or trailing spaces
    result = db.query(models.Schools).filter(
        func.lower(models.Schools.suburb) == suburb.lower(),
        func.lower(models.Schools.state) == state.lower(),
        func.lower(models.Schools.postcode) == postcode.lower()
    ).all()
    return result

def get_location_options(db: Session, keyword: str):
    if keyword != 'default':
        keyword = keyword.strip().lower()  # Trim any leading or trailing spaces and convert to lowercase
        result = db.query(models.locationOptions).filter(
            func.lower(models.locationOptions.suburb).like(f"%{keyword}%") |
            func.lower(models.locationOptions.state).like(f"%{keyword}%") |
            func.lower(models.locationOptions.postcode).like(f"%{keyword}%")
        ).distinct().limit(5)
    else:
        result = db.query(models.locationOptions).distinct().limit(5)
    return result

def get_top10(db: Session, 
              state: str = 'all', 
              sort_by: str = 'rentalYield', 
              property_type: str = 'all', 
              remoteness: str = 'all', 
              page: int = 1):
    if state == 'all':
        result = db.query(models.Suburbs).filter(
            models.Suburbs.rentalYield.isnot(None),
            models.Suburbs.annualGrowth.isnot(None)
        )
    else:
        result = db.query(models.Suburbs).filter(
            models.Suburbs.rentalYield.isnot(None),
            models.Suburbs.annualGrowth.isnot(None),
            func.lower(models.Suburbs.state) == state.lower()
        )
    
    if property_type != 'all':
        result = result.filter(func.lower(models.Suburbs.propertyType) == property_type.lower())

    if remoteness != 'all':
        result = result.filter(func.lower(models.Suburbs.remoteness_code) == remoteness.lower())

    if sort_by == 'rentalYield':
        result = result.order_by(models.Suburbs.rentalYield.desc())
    elif sort_by == 'annualGrowth':
        result = result.order_by(models.Suburbs.annualGrowth.desc())
    else:
        result = result.order_by(models.Suburbs.totalYield.desc())
    
    result = result.limit(10).offset((page-1)*10) 
    
    return result 
  

def get_total_records(db: Session, 
              state: str = 'all', 
              sort_by: str = 'rentalYield', 
              property_type: str = 'all', 
              remoteness: str = 'all'):
    if state == 'all':
        result = db.query(models.Suburbs).filter(
            models.Suburbs.rentalYield.isnot(None),
            models.Suburbs.annualGrowth.isnot(None)
        )
    else:
        result = db.query(models.Suburbs).filter(
            models.Suburbs.rentalYield.isnot(None),
            models.Suburbs.annualGrowth.isnot(None),
            func.lower(models.Suburbs.state) == state.lower()
        )
    
    if property_type != 'all':
        result = result.filter(func.lower(models.Suburbs.propertyType) == property_type.lower())

    if remoteness != 'all':
        result = result.filter(func.lower(models.Suburbs.remoteness_code) == remoteness.lower())

    if sort_by == 'rentalYield':
        result = result.order_by(models.Suburbs.rentalYield.desc())
    elif sort_by == 'annualGrowth':
        result = result.order_by(models.Suburbs.annualGrowth.desc())
    else:
        result = result.order_by(models.Suburbs.totalYield.desc())
    
    result = result.count()
    
    return {"totalRecords": result} 

def get_nearby_properties(db: Session, lat: float, lng: float, dist: int):
    result = db.query(models.Properties).filter(
        func.ST_DWithin(
            models.Properties.location,
            func.ST_GeogFromText(f'POINT({lng} {lat})'),
            dist
        )
    ).all()
    return result