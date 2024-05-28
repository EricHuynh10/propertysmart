from typing import List, Any, Union, Dict, Tuple

# from geopy.geocoders import Nominatim
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from config import cors_allowed_origins_list
from fastapi import Query
from utils import nearby_summary

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
     TrustedHostMiddleware, 
     allowed_hosts=["propertysmartbackend.azurewebsites.net", "localhost", "127.0.0.1"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/schools/', response_model=List[schemas.School])
def create_schools(schools: List[schemas.SchoolCreate], db: Session = Depends(get_db)):
    return crud.create_school(db, schools)

@app.post('/property/', response_model=List[schemas.Property])
def create_properties(properties: List[schemas.PropertyCreate], db: Session = Depends(get_db)):
    return crud.create_property(db, properties)

@app.post('/suburb/', response_model=List[schemas.Suburb])
def create_suburbs(suburbs: List[schemas.SuburbCreate], db: Session = Depends(get_db)):
    return crud.create_suburb(db, suburbs)

@app.get('/suburb/{suburb}', response_model=schemas.SuburbDetails)
async def get_suburb_details(suburb: str, db: Session = Depends(get_db)):
    try:
        # suburb is in the format of "suburb-state-postcode". Parse it
        sub = " ".join(suburb.split('-')[:-2])
        state = suburb.split('-')[-2]
        postcode = suburb.split('-')[-1]
        suburb_properties = crud.get_suburb_details(db, sub, state, postcode)
        suburb_schools = crud.get_schools_by_suburb(db, sub, state, postcode)
        if not suburb_properties:
            raise HTTPException(status_code=404, detail="Suburb not found")
        return schemas.SuburbDetails(properties=suburb_properties, schools=suburb_schools)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/location-options', response_model=List[schemas.LocationOption], tags=['location-options'])
async def get_location_options(search: str = Query('default', description='Search_value'), db: Session = Depends(get_db)):
    try:
        location_options = crud.get_location_options(db, search)
        return location_options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/top10', response_model=List[schemas.Suburb])
async def get_top10(state: str = Query('all', description='state'),
                    sortBy: str = Query('rentalYield', description='sort_by'),
                    propertyType: str = Query('all', description='property_type'),
                    remoteness: str = Query('all', description='remoteness'),
                    page: int = Query(1, description='page'),
                    db: Session = Depends(get_db)
                    ):
    try:
        top10 = crud.get_top10(db, state, sortBy, propertyType, remoteness, page)
        return top10
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/total-records', response_model=schemas.TotalRecords)
async def get_total_records(state: str = Query('all', description='state'),
                            sortBy: str = Query('rentalYield', description='sort_by'),
                            propertyType: str = Query('all', description='property_type'),
                            remoteness: str = Query('all', description='remoteness'),
                            db: Session = Depends(get_db)
                            ):
    try:
        print('check1')
        total_records = crud.get_total_records(db, state, sortBy, propertyType, remoteness)
        return total_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/property/{id}')
def get_property_id(id: int, db: Session = Depends(get_db)):
    try:
        property = crud.get_property(db, int(id))
        return property
    except Exception as e:
        return {}

@app.get('/nearby', response_model=schemas.NearbyDict)
def get_nearby_properties(lat: float = Query(..., description='latitude'), 
                          lng: float = Query(..., description='longitude'), 
                          dist: int = Query(500, description='distance'), 
                          db: Session = Depends(get_db)):
    try:
        nearby_data = crud.get_nearby_properties(db, lat, lng, dist)
        nearby_data_dict = [obj.__dict__ for obj in nearby_data]
        nearby_summary_data, tranx_LTM = nearby_summary(nearby_data_dict)
        response = { 
            'summary': nearby_summary_data,
            'transactions': tranx_LTM
        }
        return response
    except Exception as e:
        return {}



