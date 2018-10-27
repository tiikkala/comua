# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 13:47:35 2018

@author: Ilpo
"""
import pandas as pd
import numpy as np
from scipy.stats import norm
from sklearn.externals import joblib
from numpy.linalg import inv
import json

class Region:

    def __init__(self,region_name):
        self.name = region_name
        self.features = {}
        self.normalizer = 1.0
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    def add_feature(self,feature_name,means,variances,weights):
        self.features[feature_name] = {'means' : means.tolist(), 'variances' : variances.tolist(),'weights' : weights.tolist()}
    
    def set_normalizer(self,normalizer):
        self.normalizer = [normalizer]
    
    
    def build_from_dict(self,dictionary):
        self.normalizer = dictionary['normalizer']
        features = dictionary['features']
        for feature in features:
            self.features[feature] = {'means' : features[feature]['means'],'variances' : features[feature]['variances'],'weights' : features[feature]['weights'],'coefficient' : features[feature]['coefficient']}
        return self
    
    def value(self,point):
        value = 0
        i=0
        for feature in self.features:
            value += self.features[feature]['coefficient']*self.feature_pdf(point[:,i],feature)
            i+=1
        return value
    
    def feature_pdf(self,x,feature):
        values = np.zeros(x.shape)
        means = self.features[feature]['means']
        variances = self.features[feature]['variances']
        weights = self.features[feature]['weights']
        for i in range(len(means)):
            values = values + weights[i] * norm.pdf(x,means[i],variances[i])
        return values
    
    def train_responsibilities(self,x,y):
        X = np.concatenate((x,np.ones(shape=y.shape)),1)
        i = 0
        for feature in self.features:
            X[:,i]=self.feature_pdf(X[:,i],feature)
            i+=1
        coeffs = inv(X.transpose().dot(X)).dot(X.transpose()).dot(y)
        i=0
        for feature in self.features:
            self.features[feature]['coefficient'] = coeffs[i].tolist()
            i+=1

class Predictor:
    

    def __init__(self,scaler_filename = 'scaler.save',model_filename = 'model.json'):
        self.scaler_filename = scaler_filename
        self.model_filename = model_filename
        self.init_scaler()
        self.init_model()
        
    
    def init_scaler(self):
        self.scaler = joblib.load(self.scaler_filename)
    
    def init_model(self):
        self.region_objects = {}
        with open(self.model_filename,'rb') as lf:
            model = json.loads(json.load(lf))
        for region in model:
            region_object = Region(region).build_from_dict(model[region])
            self.region_objects[region] = region_object
    
    def value(self,point):
        if type(point) == 'list':
            point = np.array(point)
        point = point.reshape([1,-1])
        df = pd.DataFrame()
        x = self.scaler.transform(point)
        df['region']=np.array(list(self.region_objects.keys()))
        absolute_values = np.zeros(len(self.region_objects))
        relative_values = np.zeros(len(self.region_objects))
        for i, region in enumerate(self.region_objects):
            absolute_values[i] = self.region_objects[region].value(x)
            relative_values[i] = 100*absolute_values[i] / self.region_objects[region].normalizer
        df['absolute_values']=absolute_values
        df['relative_values']=relative_values
        return df
        
  


# =============================================================================
# THESE ARE DEFAULT NAMES AND PREDICTOR DOE NOT NEED THEM IF THEY ARE USED   
# =============================================================================
#scaler_filename = 'scaler.save'
#model_filename = 'model.json'

df = pd.read_csv('data/aggregated_data_with_features.csv')
cont_features = ['tempo','energy','liveness','duration_ms','loudness','instrumentalness','acousticness','speechiness']
df = df.dropna(subset = cont_features)
X = df.sample(1)[cont_features].values
# point is a list or numpy array with 8 values. This one is a random sample
# from the data
point = X[0,:]



# =============================================================================
# NOTE predictor.value() needs also the dataframe in order to be able to
#      calculate relative values WHICH ARE SHIT AT THE MOMENT 
# =============================================================================


predictor = Predictor()
desired_dataframe = predictor.value(point)

print(desired_dataframe)

#print(df[])
#print(predictor.value(point,df))