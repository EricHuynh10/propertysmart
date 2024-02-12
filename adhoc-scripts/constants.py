import json

import pandas as pd

# au_postcode_df = pd.read_csv('au_postcodes.csv')
# state_codes = list(au_postcode_df.state_code.unique())
# states_df = {}
# for state in state_codes:
#     states_df[state] = au_postcode_df.loc[au_postcode_df['state_code'] == state]

# folder to store all the crawed data
data_folder = "D:\\aus_real_estate_data"

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
