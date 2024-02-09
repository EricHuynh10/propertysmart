import pandas

#links to the excel files containing the postal area and suburb
meshblock_xlsx = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files/MB_2021_AUST.xlsx"
remoteness_xlsx = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files/RA_2021_AUST.xlsx"
postal_area_xlsx = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files/POA_2021_AUST.xlsx"

#download excel files and load them into a pandas dataframe
meshblock_df = pandas.read_excel(meshblock_xlsx, engine='openpyxl')
remoteness_df = pandas.read_excel(remoteness_xlsx, engine='openpyxl')
postal_area_df = pandas.read_excel(postal_area_xlsx, engine='openpyxl')

# filter the columns to only include the relevant columns
meshblock_df =  meshblock_df[['MB_CODE_2021', 'SA1_CODE_2021']]
remoteness_df = remoteness_df[['SA1_CODE_2021', 'RA_CODE_2021', 'RA_NAME_2021', 'STATE_CODE_2021', 'STATE_NAME_2021']]
postal_area_df = postal_area_df[['MB_CODE_2021', 'POA_CODE_2021']]

# merge the dataframes to create a single dataframe
suburb_remoteness_df = pandas.merge(meshblock_df, remoteness_df, on='SA1_CODE_2021')
suburb_remoteness_df = pandas.merge(suburb_remoteness_df, postal_area_df, on='MB_CODE_2021')

#rename columns
suburb_remoteness_df = suburb_remoteness_df.rename(columns={'RA_CODE_2021':'remoteness_code', 'RA_NAME_2021':'remoteness', 'POA_CODE_2021':'postcode', 'STATE_NAME_2021':'state'})

#remove duplicates and rows with null values
suburb_remoteness_df = suburb_remoteness_df.drop_duplicates()
suburb_remoteness_df = suburb_remoteness_df.dropna()

#if multiple suburbs have the same postcode, keep the first one
suburb_remoteness_df = suburb_remoteness_df.drop_duplicates(subset='postcode', keep='first')

#remove rows with postcodes that are not numbers
suburb_remoteness_df = suburb_remoteness_df[suburb_remoteness_df['postcode'].str.isnumeric()]

#remove special postcodes
suburb_remoteness_df = suburb_remoteness_df[suburb_remoteness_df['postcode'] != '9494']
suburb_remoteness_df = suburb_remoteness_df[suburb_remoteness_df['postcode'] != '9797']

#map state to state code
state_code = {
    'Northern Territory':'NT',
    'Australian Capital Territory':'ACT',
    'New South Wales':'NSW',
    'Victoria':'VIC',
    'Queensland':'QLD',
    'South Australia':'SA',
    'Western Australia':'WA',
    'Tasmania':'TAS'
}
suburb_remoteness_df['state_code'] = suburb_remoteness_df['state'].map(state_code)
suburb_remoteness_df = suburb_remoteness_df[['postcode', 'state_code', 'remoteness', 'remoteness_code']]
suburb_remoteness_df.rename(columns={'state_code': 'state'}, inplace=True)
suburb_remoteness_df['remoteness_code'] = suburb_remoteness_df['remoteness_code'].astype(str).str[1]
