import pandas as pd

country_specific_streams = pd.read_csv('data/aggregated_data.csv').drop('Unnamed: 0', axis=1)
features = pd.read_csv('data/tracks_with_features.csv').drop('Unnamed: 0', axis=1)

country_specific_streams.URL = country_specific_streams.URL.str.split('/').str[4]
country_specific_streams.rename(columns={'URL': 'id'}, inplace=True)
country_specific_streams.columns = country_specific_streams.columns.str.lower()

country_specific_streams.set_index('id', drop=False)
features.set_index('id', drop=False)

df = pd.concat([country_specific_streams, features], axis=1)

df.to_csv('data/aggregated_data_with_features.csv')