import os
import json
import re
import requests
import pandas as pd
import time
import datetime
from pydantic import BaseModel, ValidationError
from constants import data_folder

# import schemas from web/backend for data validation at migration
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(root_dir, 'web', 'backend')
sys.path.append(backend_path)
from schemas import SchoolBase


def migrate_schools():
    file = os.path.join(data_folder, "schools", "schools.csv") #local directory where the data is stored
    url = 'http://localhost:8000/schools' # backend url to post data

    with open(file) as f:
        schools_df = pd.read_csv(f)

    schools_df = schools_df.drop_duplicates(subset=['school', 'suburb', 'state', 'postcode', 'educationLevel'], keep='first')
    batch_data = []
    for _, row in schools_df.iterrows():
        try:
            school_data = SchoolBase(
            school=row['school'],
            suburb=row['suburb'],
            state=row['state'],
            postcode=str(row['postcode']),
            schoolType=row['schoolType'],
            educationLevel=row['educationLevel'],
            score=row['score'] if str(row['score']).isnumeric() else None
            )

            school_data = school_data.model_dump()
            batch_data.append(school_data)

        except ValidationError as e:
            print(e)
            
    # Send data
    try:
        if batch_data:
            r = requests.post(url, json=batch_data)
            print(r.status_code, r.reason)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    migrate_schools()

