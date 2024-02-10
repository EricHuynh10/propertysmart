import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
from io import StringIO
from constants import au_postcodes_df
from pydantic import BaseModel
from typing import Optional
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def crawl_school():
    schools_df = extract_school_from_suburb_profile()
    schools_df.sort_values(by=['postcode'], inplace=True)

    schools_with_score_df = crawl_school_from_better_education()
    QLD_schools_with_score_df = schools_with_score_df[schools_with_score_df['postcode']==""].copy()

    # Function to apply fuzzy matching
    def get_best_match_suburb(row):
        name = str(row['suburb'])
        choices = au_postcodes_df[au_postcodes_df['state'] == row['state']]['suburb']
        best_match = process.extractOne(name, choices)
        if not best_match:
            return None
        return best_match[0]  # Returns the best match name
    
    QLD_schools_with_score_df['bestmatchsuburb'] = QLD_schools_with_score_df.apply(get_best_match_suburb, axis=1)
    QLD_schools_with_score_df.drop(columns=['postcode', 'suburb'], inplace=True)
    QLD_schools_with_score_df.rename(columns={'bestmatchsuburb': 'suburb'}, inplace=True)

    au_postcodes_df_copy = au_postcodes_df.copy()
    au_postcodes_df_copy.drop_duplicates(subset=['state', 'suburb'], keep="first", inplace=True)

    QLD_schools_with_score_df = QLD_schools_with_score_df.merge(au_postcodes_df_copy, on=['suburb', 'state'], suffixes=('_l', '_r'), how='left')

    schools_with_score_df = schools_with_score_df[['school', 'suburb', 'state', 'postcode', 'score', 'school_type', 'educationLevel']]
    QLD_schools_with_score_df = QLD_schools_with_score_df[['school', 'suburb', 'state', 'postcode', 'score', 'school_type', 'educationLevel']]
    schools_with_score_df = pd.concat([schools_with_score_df[schools_with_score_df['state']!='QLD'], QLD_schools_with_score_df], ignore_index=True)

    def preprocess_school_names(name):
    # For example, lowercasing, removing common suffixes/prefixes, etc.
        name.lower()
        name = name.replace('primary', '')
        name = name.replace('secondary', '')
        name = name.replace('school', '')
        name = name.replace('college', '')
        name = name.replace('public', '')
        name = name.replace('private', '')
        return name

    # Function to apply fuzzy matching
    def get_best_match_school(row):
        name = row['school_cleaned']
        choices = schools_df[(schools_df['postcode'] == str(row['postcode'])) & (schools_df['educationLevel'] == row['educationLevel'])]['school_cleaned']
        best_match = process.extractOne(name, choices, score_cutoff=80)
        if not best_match:
            return None
        return best_match[0]  # Returns the best match name

    # Apply preprocessing
    schools_with_score_df['school_cleaned'] = schools_with_score_df['school'].apply(preprocess_school_names)
    schools_df['school_cleaned'] = schools_df['school'].apply(preprocess_school_names)

    schools_with_score_df['BestMatchName'] = schools_with_score_df.apply(get_best_match_school, axis=1)

    # add a column calculating similarity between school_cleaned and BestMatchName
    schools_with_score_df['similarity'] = schools_with_score_df.apply(lambda row: fuzz.ratio(row['school_cleaned'], row['BestMatchName']), axis=1)
    schools_with_score_df[(schools_with_score_df.duplicated(subset=['BestMatchName', 'postcode', 'educationLevel'], keep=False)) & (schools_with_score_df['state']=="NSW")].sort_values(by=['BestMatchName', 'postcode', 'educationLevel', 'similarity'], ascending=False)

    schools_with_score_df = schools_with_score_df.sort_values(by=['BestMatchName', 'postcode', 'educationLevel', 'similarity'], ascending=False)
    schools_with_score_df.drop_duplicates(subset=['BestMatchName', 'postcode', 'educationLevel'], keep='first', inplace=True)
    schools_with_score_df = schools_with_score_df[schools_with_score_df['BestMatchName'].notnull()]
    schools_with_score_df = schools_with_score_df[schools_with_score_df['similarity'] >= 80]
    #concate 3 columns bestmatchname, postcode, educationLevel to create a unique key
    schools_with_score_df['key'] = schools_with_score_df['BestMatchName'].astype(str) + schools_with_score_df['postcode'].astype(str) + schools_with_score_df['educationLevel'].astype(str)

    schools_df['key'] = schools_df['school_cleaned'].astype(str) + schools_df['postcode'].astype(str) + schools_df['educationLevel'].astype(str)
    final = pd.merge(schools_df, schools_with_score_df, how='left', left_on=['key'], right_on=['key'], suffixes=('_l', '_r'))
    final[final['school_cleaned_r'].notnull()].drop_duplicates(subset=['school_cleaned_l', 'postcode_l', 'educationLevel_l'], keep='first')

    final = final[['school_l', 'suburb_l', 'state_l', 'postcode_l', 'score_r', 'schoolType', 'educationLevel_l']]
    final.rename(columns={'school_l': 'school', 'suburb_l': 'suburb', 'state_l': 'state', 'postcode_l': 'postcode', 'score_r': 'score', 'educationLevel_l': 'educationLevel'}, inplace=True)

    final.drop_duplicates(subset=['school', 'postcode', 'educationLevel'], keep='first', inplace=True)
    #final.to_csv('D:\\aus_real_estate_data\schools\schools.csv', index=False)
    final.to_csv('schools.csv', index=False)
    print("Successfully crawled schools data")


def crawl_school_from_better_education():

    school_types = ['primary', 'secondary']
    states = list(au_postcodes_df['state'].unique())

    # create an empty DataFrame to store the data
    schools_with_score_df = pd.DataFrame(columns=['school', 'suburb', 'state', 'postcode', 'score', 'school_type'])

    for school_type in school_types:
        for state in states:

            print(f"Start scraping  the webpage: {school_type} {state}")

            url = f'https://bettereducation.com.au/school/{school_type}/{state}/{state}_top_{school_type}_schools.aspx'
            response = requests.get(url)

            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GridView1'})
                table_io = StringIO(str(table))

                # Convert the table to a DataFrame
                df = pd.read_html(table_io)[0]
                
                # Clean the DataFrame
                if state == 'VIC':
                    df = df.rename(columns={'Postcode': 'postcode'})
                    df['suburb'] = df['School'].str.split(',', expand=True).iloc[:, -3:-2]
                if state == 'ACT' or state == 'TAS':
                    df[['suburb', 'state', 'postcode']] = df['School'].str.split(',', expand=True).iloc[:, -3:]
                if state == 'QLD':
                    df['postcode'] = ''
                    df["suburb"] = df['Locality']
                if state == 'SA' or state == 'NT' or state == 'NSW':
                    df[['suburb', 'state', 'postcode']] = df['Locality'].str.split(',', expand=True).iloc[:, 0:3]
                if state == 'WA':
                    if school_type == 'primary':
                        df[['suburb', 'state', 'postcode']] = df['Locality'].str.split(',', expand=True).iloc[:, 0:3]
                    if school_type == 'secondary':
                        df = df.rename(columns={'Postcode': 'postcode'})
                        df['suburb'] = df['School'].str.split(',', expand=True).iloc[:, -3:-2]
                
                #handle special cases
                if school_type == 'primary':
                    if state == 'NSW':
                        df.loc[df['School'] == 'Redlands,Cremorne,NSW,2090', ['suburb', 'state', 'postcode']] = ['Cremorne', 'NSW', '2090']
                    if state == 'NT':
                        df.loc[df['Locality'] == 'Berrimah,NT,828', 'postcode'] = '0828'
                if school_type == 'secondary':
                    if state == 'NSW':
                        df.loc[df['Locality'] == 'Surry Hills NSW 2010', ['suburb', 'state', 'postcode']] = ['Surry Hill', 'NSW', '2010']
                        df.loc[df['Locality'] == 'St Ives,St Ives,NSW,2075', ['suburb', 'state', 'postcode']] = ['St Ives', 'NSW', '2075']
                        df.loc[df['School'] == 'Redlands,Cremorne,NSW,2090', ['suburb', 'state', 'postcode']] = ['Cremorne', 'NSW', '2090']


                df['School'] = df['School'].str.split(',', expand=True).iloc[:, 0]
                df["state"] = state 
                df = df[['School', 'suburb', 'state', 'postcode', 'State Overall Score']]
                df = df.rename(columns={'School': 'school', 'State Overall Score': 'score'})
                df['educationLevel'] = school_type

                # assign the dataframe name df_school_type
                schools_with_score_df = pd.concat([schools_with_score_df, df], ignore_index=True)
                
                print(f"Successfully retrieved the webpage: {school_type} {state}")
            else:
                print(f"Failed to retrieve the webpage: status code {response.status_code}")

    return schools_with_score_df


def extract_school_from_suburb_profile():
    directory = os.path.join("D:\\aus_real_estate_data", 'suburb-profile')
    states = os.listdir(directory)
    url = 'http://localhost:8000/schools' # backend url to post data

    schools_df = pd.DataFrame(columns=['school', 'suburb', 'state', 'postcode', 'schoolType', 'educationLevel', 'score'])

    for state_code in states:
        d2 = os.path.join(directory, state_code)
        suburbs = os.listdir(d2)
        
        for suburb in suburbs:
            d3 = os.path.join(d2, suburb)
            json_files = os.listdir(d3)

            # Add missing import for json module

            for json_f in json_files:
                with open(os.path.join(d3, json_f)) as f:
                    suburb_profile = json.load(f)

                try:
                    schools = suburb_profile['props']['pageProps']['details'].get('schoolCatchment', {}).get('schools')
                    # Add a check for the existence of the 'schools' key before accessing it
                    if schools:
                        for school in schools:
                            school_data = SchoolBase(
                                school=school['name'],
                                suburb=" ".join(suburb.split('-')[0:-1]),
                                state=state_code,
                                postcode=str(suburb.split('-')[-1]),
                                schoolType=school['type'],
                                educationLevel=school['educationLevel'],
                                score=None
                            )

                            school_data = school_data.model_dump()
                            if school_data['educationLevel'] == 'combined':
                                school_data['educationLevel'] = 'primary'
                                schools_df = pd.concat([schools_df, pd.DataFrame([school_data])], ignore_index=True)
                                school_data['educationLevel'] = 'secondary'
                                schools_df = pd.concat([schools_df, pd.DataFrame([school_data])], ignore_index=True)
                            else:
                                schools_df = pd.concat([schools_df, pd.DataFrame([school_data])], ignore_index=True)
                except KeyError as e:
                    continue
        
    return schools_df


class SchoolBase(BaseModel):
    school: str
    suburb: str
    state: str
    postcode: str
    schoolType: str
    educationLevel: str
    score: Optional[int] = None


# default header for the request
def header(url):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'max-age=0',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    return headers


if __name__ == "__main__":
    crawl_school()
