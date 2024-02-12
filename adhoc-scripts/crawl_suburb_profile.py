import os
import requests
from constants import au_postcodes_df
import json
import concurrent.futures
import datetime
from bs4 import BeautifulSoup
from constants import data_folder

today = datetime.date.today().strftime("%Y-%m-%d")

# function to crawl the data from domain.com.au
def crawl_suburb_profile():

    url = "https://www.domain.com.au/suburb-profile/{suburb}-{state}-{postcode}"

    def download_suburb(suburb, state, postcode):
        download_url = url.format(suburb = suburb.replace(' ', '-').lower(), state=state.lower(), postcode=postcode)
        response = requests.get(download_url, headers=header(download_url))

        #create the folder to store the data
        if response.status_code == 200:
            folder_name = os.path.join(data_folder, "suburb-profile", state, "-".join([suburb, str(postcode)]))
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find_all('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
                json_str = script_tag[0].string if script_tag else ''
                data = json.loads(json_str)
                file_name = '{date}_{state}_{suburb}_{postcode}.json'.format(state=state, suburb=suburb, postcode=postcode, date=today)
                with open(os.path.join(folder_name, file_name), 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                print('Finish {}_{}_{}'.format(state, suburb, postcode))

            except Exception as e:
                write_to_log_file('crawl_suburb_log.txt', 'Skip {}_{}_{}. {e}. Link: {}.'.format(suburb, state, postcode, e, download_url))
                print('Skip {}_{}_{}. {e}. Link: {}.'.format(suburb, state, postcode, e, download_url))
                print(download_url)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i, row in enumerate(au_postcodes_df.itertuples()):
            suburb, state, postcode = row.suburb, row.state, row.postcode
            future = executor.submit(download_suburb, suburb, state, postcode)
            futures.append(future)
            if (i+1) % 100 == 0 or (i+1) == len(au_postcodes_df):
                concurrent.futures.wait(futures)
                futures = []
                

# function to write a to a log file
def write_to_log_file(log_file, message):
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
    with open(log_file, 'a') as f:
        f.write(message + '\n')


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


if __name__ == '__main__':
    crawl_suburb_profile()