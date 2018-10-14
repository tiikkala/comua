import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

data = pd.read_csv("data/aggregated_data_with_features.csv")
descr = data.describe()

# Features described in
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

categorical_values = ["key", "mode", "time_signature"]

# Turn categorical values into numbers instead of strings
for val in categorical_values:
    data[val] = data[val].astype('category')

scatter_matrix(data, alpha=0.2, figsize = (50, 50), diagonal='kde')
