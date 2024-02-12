import os
import requests
from constants import data_folder, au_postcodes_df, listing_types, property_types
import json
import time
import pandas as pd
import concurrent.futures
import datetime

today = datetime.date.today().strftime("%Y-%m-%d")

# function to crawl the data from domain.com.au
def crawl_realestate(listing_type, property_type):
    """
    Crawl the data from domain.com.au
    :param listing_type: the type of listing as per domain.com.au
    :param property_type: the type of property to crawl
    """

    #define the url
    url = url = 'https://www.domain.com.au/{listing_type}/{suburb}-{state}-{postcode}/?ptype={property_type}&?excludepricewithheld=1&ssubs=0&sort=solddate-desc&page={page}'

    for row in au_postcodes_df.itertuples():
        suburb, state, postcode = row.suburb, row.state, row.postcode
        if state != 'ACT':
            continue
        print('Start {}_{}_{}'.format(state, suburb, postcode))

        #download the first page to get the total number of pages
        page = 1
        download_url = url.format(listing_type=listing_type, 
                                    property_type=property_type, 
                                    suburb = suburb.replace(' ', '-').lower(),
                                    state=state.lower(),
                                    postcode=postcode, 
                                    page=page)
        response = requests.get(download_url, headers=header(url))
        try:
            data = response.json()
            total_pages = data['props']['totalPages']
            first_result_address = next(iter(data['props']['listingsMap'].values()))['listingModel']['address']
            suburb = first_result_address['suburb']
            state = first_result_address['state']
        except:
            write_to_log_file('crawl_log.txt', 'Skip {}_{}_{}. {}'.format(suburb, state, postcode, download_url))
            print('Skip {}_{}_{}. {}'.format(suburb, state, postcode, download_url))
            print(download_url)
            continue

        #create the folder to store the data
        folder_name = os.path.join(data_folder, "properties")
        folder_name = os.path.join(folder_name, listing_type, state, "-".join([suburb, str(postcode)]), property_type)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        #if os path exists and contains the same number of pages, skip
        elif os.path.exists(folder_name) and len(os.listdir(folder_name)) == total_pages:
            write_to_log_file('crawl_log.txt', 'Skip {}_{}_{}. Data exists.'.format(suburb, state, postcode))
            print('Skip {}_{}_{}. Data exists.'.format(suburb, state, postcode))
            continue
        
        def download_page(page):
            download_url = url.format(listing_type=listing_type, 
                                        property_type=property_type, 
                                        suburb = suburb.replace(' ', '-').lower(),
                                        state=state.lower(),
                                        postcode=postcode, 
                                        page=page)
            response = requests.get(download_url, headers=header(url))
            try:
                data = response.json()
                data = data['props']['listingsMap']
                data = {key: {'id': value['id'],
                            'features': value['listingModel']['features'],
                            'address': value['listingModel']['address'],
                            'price': value['listingModel']['price'],
                            'tags': value['listingModel']['tags'],
                            } for key, value in data.items()}
                file_name = '{date}_{state}_{suburb}_{postcode}_{page}.json'.format(state=state, suburb=suburb, postcode=postcode, page=page, date=today)
                with open(os.path.join(folder_name, file_name), 'w') as f:
                    json.dump(data, f, indent=4)
                write_to_log_file('crawl_log.txt', 'Finish {}_{}'.format(postcode, page))
                print('Finish {}_{}_{}_{}'.format(state, suburb, postcode, page))
            except:
                write_to_log_file('crawl_log.txt', 'Skip {}_{}_{}_{}'.format(state, suburb, postcode, page))
                print('Skip {}_{}_{}_{}'.format(state, suburb, postcode, page))
                print(download_url)

        #download the data for each page
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for page in range(1, total_pages + 1):
                future = executor.submit(download_page, page)
                futures.append(future)
            concurrent.futures.wait(futures)

        print('Finish {}_{}_{}'.format(state, suburb, postcode))
        time.sleep(0.5)
        

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

    for listing_type in listing_types:
        for property_type in property_types:
            crawl_realestate(listing_type, property_type)
            
