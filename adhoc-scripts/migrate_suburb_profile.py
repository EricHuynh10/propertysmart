import os
import json
import pandas as pd
import numpy as np
import requests

from suburb_remoteness import suburb_remoteness_df

def migrate_suburb_profile():
    directory = "D:\\aus_real_estate_data\\suburb-profile" # directory where suburb profile data is stored
    url = 'http://localhost:8000/suburb/' # url to post data to db
    states = os.listdir(directory)

    suburb_data_df = pd.DataFrame()

    for state_code in states:
        d2 = os.path.join(directory, state_code)
        suburbs = os.listdir(d2)

        for suburb in suburbs:
            d3 = os.path.join(d2, suburb)
            json_files = os.listdir(d3)
            suburb, postcode = suburb[:-5], suburb[-4:]

            # Add missing import for json module
            for json_f in json_files:
                with open(os.path.join(d3, json_f)) as f:
                    suburb_profile = json.load(f)
                
                try:
                    mkt_insights = suburb_profile['props']['pageProps']['details']['marketInsights']
                except:
                    continue
                
                for value in mkt_insights:
                    temp = {}
                    temp['state'] = state_code
                    temp['suburb'] = suburb
                    temp['postcode'] = postcode
                    temp['beds'] = value['beds']
                    temp['propertyType'] = value['propertyType']
                    temp['medianPrice'] = value['medianPrice'] if value['medianPrice'] > 0 else np.nan
                    temp['medianRent'] = value['medianRentPrice'] if value['medianRentPrice'] > 0 else np.nan
                    temp['avgDaysOnMarket'] = value['avgDaysOnMarket'] if value['avgDaysOnMarket'] > 0 else np.nan
                    temp['soldThisYear'] = value['nrSoldThisYear']
                    temp['entryLevelPrice'] = value['entryLevelPrice'] if value['entryLevelPrice'] > 0 else np.nan
                    temp['luxuryLevelPrice'] = value['luxuryLevelPrice'] if value['luxuryLevelPrice'] > 0 else np.nan
                    temp['annualGrowth'] = np.nan
                    for i in value['salesGrowthList']:
                        if i['year'] == '2023':
                            temp['annualGrowth'] = i['annualGrowth'] if i['annualGrowth'] > 0 else np.nan
                    
                    suburb_data_df = pd.concat([suburb_data_df, pd.DataFrame([temp])], ignore_index=True)
            
            print('Finished processing suburb:', suburb, 'postcode:', postcode, 'state:', state_code)

    suburb_data_df['rentalYield'] = (suburb_data_df['medianRent'] * 52) / suburb_data_df['medianPrice']
    suburb_data_df['totalYield'] = suburb_data_df['rentalYield'] + suburb_data_df['annualGrowth']
    suburb_data_df = pd.merge(suburb_data_df, suburb_remoteness_df, on=['postcode', 'state'], how='left')

    #suburb_data_df.to_csv('suburb_data.csv', index=False)
    suburb_data_json = json.loads(suburb_data_df.to_json(orient='records'))
    r = requests.post(url, json=suburb_data_json)
    if r.status_code == 200:
        print('Suburb data migrated successfully')
    else:
        print(r.status_code, r.reason)

if __name__ == "__main__":
    migrate_suburb_profile()

