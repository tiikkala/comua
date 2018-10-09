from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import time
import pandas as pd

# Get audio features for our dataset consisting of 200 most streamed track per country from the
# Spotify API

print("Loading data")
df = pd.read_csv("data/aggregated_data.csv")
print("Done.")

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True

chunk_size = 50
tids = df['URL']
tid_chunks = [tids[i:i+chunk_size] for i in range(0, len(tids), chunk_size)]

number_of_tracks = len(tids.values)
counter = 0
features = pd.DataFrame()
for chunk in tid_chunks:
    start = time.time()
    for row in sp.audio_features(chunk):
        features = features.append(pd.Series(row), ignore_index=True)
        counter = counter + 1
    print("Features for %s / %s tracks fetched" % (counter, number_of_tracks))

features.to_csv('data/tracks_with_features.csv')