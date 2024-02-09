import os
import json
import re
import requests
import pandas as pd
import time
import datetime
from pydantic import BaseModel, ValidationError

# import schemas from web/backend for data validation at migration
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(root_dir, 'web', 'backend')
sys.path.append(backend_path)
from schemas import PropertyBase


def migrate_property_data():
    directory = "D:\\aus_real_estate_data\properties\sold-listings" #local directory where the data is stored
    #states = os.listdir(directory)
    states = ['VIC', 'WA'] # states to process
    url = 'http://localhost:8000/property' # backend url to post data
    

    for state_code in states:
        d2 = os.path.join(directory, state_code)
        suburbs = os.listdir(d2)

        start_time = time.time()

        # create pandas dataframe to store data with data types in line with the backend schema
        state_data = []

        
        for suburb in suburbs:
            print(f'Processing suburb: {state_code}-{suburb}')
            d3 = os.path.join(d2, suburb)
            property_types = os.listdir(d3)

            for property_type in property_types:
                d4 = os.path.join(d3, property_type)
                json_files = os.listdir(d4)
                
                for json_f in json_files:
                    with open(os.path.join(d4, json_f)) as f:
                        page = json.load(f)
                    for _, value in page.items():
                        try:
                            tagText=value['tags'].get('tagText')
                            try:
                                soldDate = re.findall(r'\d{1,2}\s\w{3}\s\d{4}', tagText)[0]
                                soldDate = datetime.datetime.strptime(soldDate, '%d %b %Y').strftime('%Y-%m-%d')
                            except IndexError:
                                soldDate = None
                                continue

                            if value['price'] == "Price Withheld":
                                continue

                            property_data = PropertyBase(
                                property_id=value['id'],
                                beds=value['features'].get('beds'),
                                baths=value['features'].get('baths'),
                                parking=value['features'].get('parking'),
                                propertyType=value['features'].get('propertyType'),
                                propertyTypeFormatted=value['features'].get('propertyTypeFormatted'),
                                isRural=value['features'].get('isRural'),
                                landSize=value['features'].get('landSize'),
                                landUnit=value['features'].get('landUnit'),
                                isRetirement=value['features'].get('isRetirement'),
                                street=value['address'].get('street'),
                                suburb=value['address'].get('suburb'),
                                state=value['address'].get('state'),
                                postcode=value['address'].get('postcode'),
                                lat=value['address'].get('lat'),
                                lng=value['address'].get('lng'),
                                price=int(re.sub(r'[$,]', '', value['price'])),
                                tagText=value['tags'].get('tagText'),
                                tagClassName=value['tags'].get('tagClassName'),
                                soldDate=soldDate
                            )

                            property_data = property_data.model_dump()
                            if property_data['soldDate'] != None:
                                property_data['soldDate'] = str(property_data['soldDate']) #convert date to ISO 8601 format. Date type is not supported by JSON
                            state_data.append(property_data)

                        except ValidationError as e:
                            msg = f"Validation error for record: {state_code}, {suburb}, {property_type}, {json_f}, {value['id']}: {str(e)}"
                            write_to_log_file('migration_db_log.txt', msg)
                            print(msg)

        print("Finished compiling data for: {}. Total records {}. Sending data.".format(state_code, len(state_data)))
        print(f"Total time taken to process data for {state_code} is {time.time() - start_time}")

        # Clean data before posting to backend
        if state_data:
            state_data_df = pd.DataFrame(state_data).astype('object')
            state_data_df = state_data_df.where(pd.notnull(state_data_df), None)
            state_data_df = state_data_df.drop_duplicates(subset=['property_id', 'street', 'suburb', 'state', 'postcode', 'soldDate'], keep='first')
            state_data_df = state_data_df.dropna(subset=['property_id', 'soldDate'])


            state_data_cleaned = []
            for _, row in state_data_df.iterrows():
                row = row.to_dict()
                try:
                    property_data = PropertyBase(
                        property_id=row['property_id'],
                        beds=row['beds'],
                        baths=row['baths'],
                        parking=row['parking'],
                        propertyType=row['propertyType'],
                        propertyTypeFormatted=row['propertyTypeFormatted'],
                        isRural=row['isRural'],
                        landSize=row['landSize'],
                        landUnit=row['landUnit'],
                        isRetirement=row['isRetirement'],
                        street=row['street'],
                        suburb=row['suburb'],
                        state=row['state'],
                        postcode=row['postcode'],
                        lat=row['lat'],
                        lng=row['lng'],
                        price=row['price'],
                        tagText=row['tagText'],
                        tagClassName=row['tagClassName'],
                        soldDate=row['soldDate']
                    )

                    property_data = property_data.model_dump()
                    if property_data['soldDate'] != None:
                        property_data['soldDate'] = str(property_data['soldDate']) #convert date to ISO 8601 format. Date type is not supported by JSON
                    state_data_cleaned.append(property_data)
                except ValidationError as e:
                    print(row)
            
            print(f"Total records after cleaning: {len(state_data_cleaned)}")

            #split state data into batches of 10000 records
            batch_size = 10000
            batch_data = [state_data_cleaned[i:i + batch_size] for i in range(0, len(state_data_cleaned), batch_size)]

            # send data
            for batch in batch_data:
                try:
                    r = requests.post(url, json=batch)
                    print(f"Current batch: {state_code}. Batch size: {len(batch)}")
                    print(f"HTTP request status: {r.status_code}, {r.reason}")
                except Exception as e:
                    write_to_log_file('migration_db_log.txt', str(e))
                    print(e)

        end_time = time.time()
        print(f'Total time taken for is {end_time - start_time}. State: {state_code}. Total records: {len(state_data_cleaned)}')


# function to write a to a log file
def write_to_log_file(log_file, message):
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
    with open(log_file, 'a') as f:
        f.write(str(message) + '\n')


if __name__ == "__main__":
    migrate_property_data()