# Get audio features for given URLs in chunks of 50

from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import sys
import pandas as pd

print("Loading data")
data = pd.read_csv("spotifys-worldwide-daily-song-ranking/data.csv")
print("Done.")

data = data.head(200)

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True

tids = []
for tid in data['URL']:
    tids.append(tid)

chunk_size = 50
tid_chunks = [tids[i:i+chunk_size] for i  in range(0, len(tids), chunk_size)]

features = []
for chunk in tid_chunks:
    for row in sp.audio_features(chunk):
        features.append(row)

# Make data frame
features_df = pd.DataFrame(features)

# TODO: combine with original data df

print(features_df)
