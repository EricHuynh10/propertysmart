import pandas as pd

# folder to store all the crawed data
data_folder = "D:\\aus_real_estate_data"

# backend url to post data
backend_url = "https://propertysmart-backend.azurewebsites.net"

# import the aus_postcode.csv file
data_types = {
    'suburb': 'str',
    'state': 'str',
    'postcode': 'str',
}
au_postcodes_df = pd.read_csv('au_postcode_domain.csv', dtype=data_types)

# define property types and listing types on domain.com.au
listing_types = ['sold-listings']
property_types = ['apartment', 'house', 'town-house', 'development-site,new-land,vacant-land']
