import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os
from constants import states_df

def crawl_school():

    school_types = ['primary', 'secondary']
    states = list(states_df.keys())

    if not os.path.exists(os.path.join('data','schools')):
        os.makedirs(os.path.join('data','schools'))
    else:
        for file_name in os.listdir(os.path.join('data','schools')):
            os.remove(os.path.join('data','schools', file_name))

    for school_type in school_types:
        for state in states:

            print(f"Start retrieving the webpage: {school_type} {state}")
            # The URL of the page you want to scrape
            url = f'https://bettereducation.com.au/school/{school_type}/{state}/{state}_top_{school_type}_schools.aspx'

            # Fetch the page
            response = requests.get(url)

            # Check if the request was successful
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

                # Save the DataFrame to a CSV file
                file_name = f'{school_type}.csv'
                folder_name = os.path.join('data', 'schools')
                header = True if not os.path.exists(os.path.join(folder_name, file_name)) else False
                df.to_csv(os.path.join(folder_name, file_name), index=False, mode='a', header=header)
                
                print(f"Successfully retrieved the webpage: {school_type} {state}")
            else:
                print(f"Failed to retrieve the webpage: status code {response.status_code}")
    
if __name__ == "__main__":
    crawl_school()
