import pandas as pd

def nearby_summary(data: dict):
  if len(data) == 0:
    return {}
  df = pd.DataFrame(data)
  df['propertyType'] = df['propertyType'].apply(lambda x: 'Unit' if x == 'ApartmentUnitFlat' else x)
  df['soldDate'] = pd.to_datetime(df['soldDate'])
  maxDate = df['soldDate'].max()
  L12MDate = df['soldDate'].max() - pd.DateOffset(months=12)
  L12MDate_prev = df['soldDate'].max() - pd.DateOffset(months=24)
  df_L12M = df[(df['soldDate'] >= L12MDate) & (df['soldDate'] <= maxDate)]
  df_L12M_prev = df[(df['soldDate'] >= L12MDate_prev) & (df['soldDate'] <= L12MDate)]
  grouped_df_L12M = df_L12M.groupby(['propertyType', 'beds']).agg(
    medianPrice=('price', 'median'),
    TranxLTM=('price', 'count')
  )
  grouped_df_L12M_prev = df_L12M_prev.groupby(['propertyType', 'beds']).agg(
    medianPrice=('price', 'median'),
    TranxLTM=('price', 'count')
  )
  joined_df = grouped_df_L12M.join(grouped_df_L12M_prev, on=['propertyType', 'beds'], lsuffix='_L12M', rsuffix='_L12M_prev')
  joined_df = joined_df.fillna(-1)  # Replace NaN values with '-'
  joined_dict = joined_df.to_dict(orient='index')

  df_L12M = df_L12M.fillna(-1)
  df_L12M = df_L12M.sort_values(by='soldDate', ascending=False)
  return joined_dict, df_L12M.to_dict(orient='records')