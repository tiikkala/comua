import pandas as pd

# Aggregate date level data country level as time-dimension is not used in analysis

df = pd.read_csv("data/spotifys-worldwide-daily-song-rankings.csv")

df = df.drop(['Position', 'Date'], axis=1)
df = df.groupby(['Region', 'URL'], as_index=False).agg({'Streams': sum, 'Track Name': 'first', 'Artist': 'first'})

df.to_csv('data/aggregated_data.csv')