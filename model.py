#note: temp readings are 20s apart

import pandas as pd
import os
import matplotlib.pyplot as plt
import random
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Normalization
import numpy as np
import sys
import csv

os.chdir('data')

# dictionary of dataframes:
dfs = {}

for folder in os.listdir():
    if os.path.isdir(folder):
        os.chdir(folder)
        for file in os.listdir():
            if file.startswith('~'):
                continue
            df = pd.read_excel(file, sheet_name="DATA", usecols='C,D', skiprows = 1)
            df.columns = ['temp', 'label']
            # to ensure that there are breaks between each recorded shower:
            df.loc[df.shape[0]] = [None, None]
            dfs[file] = df
        os.chdir('..')

# concatenating all our data into one big dataframe:
data = pd.concat(list(dfs.values()), ignore_index = True)

# start window size: 19
# end window size: 25
start_pts = []#list where the first item is 1 for start and 0 for not start
end_pts = []#same list but for ends

for i, row in data.iterrows():
    if not pd.isnull(row['label']):
        if row['label'].startswith('Start'):
            start_pts.append([1] + data.iloc[i-9:i+10]['temp'].tolist())
        if row['label'].startswith('End'):
            end_pts.append([1] + data.iloc[i-12:i+13]['temp'].tolist())
initial_length = len(start_pts)
if initial_length != len(end_pts):
    print("inconsistent labels!")

#taking a random sample of indices (without replacement) of size k
random_start_indices = random.sample(range(len(data) - 19), k =  len(data) - 19)
random_end_indices = random.sample(range(len(data) - 25), k = len(data) - 25)

for i in random_start_indices:
    if not (any(pd.isnull(data.iloc[i:i+19//2]['temp'])) or
            (not pd.isnull(data.iloc[i+19//2]['label']) and data.iloc[i+19//2]['label'].startswith('Start'))):
        start_pts.append([0] + data.iloc[i:i+19]['temp'].tolist())
        if len(start_pts) == initial_length * 2:
            break

for i in random_end_indices:
    if not (any(pd.isnull(data.iloc[i:i+25//2]['temp'])) or
            (not pd.isnull(data.iloc[i+25//2]['label']) and data.iloc[i+25//2]['label'].startswith('End'))):
        end_pts.append([0] + data.iloc[i:i+25]['temp'].tolist())
        if len(end_pts) == initial_length * 2:
            break

#tensors holding the label, followed by a list of 10 temperatures:
start_data = np.asarray(start_pts)
np.random.shuffle(start_data)

end_data = np.asarray(end_pts)
np.random.shuffle(end_data)

data_length = start_data.shape[0]

start_train = start_data[:int(data_length * .7)]
start_val = start_data[int(data_length * .7):int(data_length * .85)]
start_test = start_data[int(data_length * .85):]

end_train = end_data[:int(data_length * .7)]
end_val = end_data[int(data_length * .7):int(data_length * .85)]
end_test = end_data[int(data_length * .85):]


n = sys.argv[0]

start_model = Sequential(
    [
        BatchNormalization(),
        Dense(2**n, activation = 'relu', input_shape=(19,)),
        Dense(1, activation = 'sigmoid')
    ]
)

start_model.compile(
    loss='mse',
    metrics=['mae'],
    optimizer = Adam(learning_rate=1e-5)
)

history = start_model.fit(
    start_train[:,1:],
    start_train[:,0],
    epochs = int(1e6),
    validation_data = (start_val[:,1:], start_val[:,0]),
    verbose = 0
)

end_model = Sequential(
    [
        BatchNormalization(),
        Dense(2**n, activation = 'relu', input_shape=(25,)),
        Dense(1, activation = 'sigmoid')
    ]
)

end_model.compile(loss='mse', metrics=['mae'])
end_model.fit(end_train[:,1:], end_train[:,0], epochs=2000)
end_val_predicted = end_model.predict(end_val[:,1:])

start_maes.append(np.mean(np.absolute(start_val_predicted[:,0] - start_val[:,0])))
end_maes.append(np.mean(np.absolute(end_val_predicted[:,0] - end_val[:,0])))

