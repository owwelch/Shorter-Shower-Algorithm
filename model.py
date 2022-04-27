# note: temp readings are 20s apart
# takes in input n for the number of neurons
import pandas as pd
import os
import matplotlib.pyplot as plt
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
import numpy as np
import sys

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

# is this a start or end model?
model_type = sys.argv[1]


if model_type == 'Start':
    window_size = 19
elif model_type == 'End':
    window_size = 25
else:
    raise ValueError("invalid model type. 2nd argument must be either 'Start' or 'End'.")

#list where the first item is 1 for model_type and 0 for not model_type:
pts = []

for i, row in data.iterrows():
    if not pd.isnull(row['label']):
        if row['label'].startswith(model_type):
            pts.append([1] + data.iloc[i-window_size//2:i+window_size//2+1]['temp'].tolist())

initial_length = len(pts)

#taking a random sample of indices (without replacement) of size k
random_indices = random.sample(range(len(data) - window_size), k =  len(data) - window_size)

i = 0
for _ in range(initial_length):
    # none of the temp data can be null, and the midpoint can't be a pointed labeled with the model type.
    while any(pd.isnull(data.iloc[i:i+window_size]['temp'])) or (
        not pd.isnull(data.iloc[i+window_size//2]['label']) and data.iloc[i+window_size//2]['label'].startswith(model_type)
    ):
        i += 1
    pts.append([0] + data.iloc[i:i+19]['temp'].tolist())
    i += 1


#tensors holding the label, followed by a list of 10 temperatures:
data = np.asarray(pts)
np.random.shuffle(data)

data_length = data.shape[0]

train = data[:int(data_length * .7)]
val = data[int(data_length * .7):int(data_length * .85)]
test = data[int(data_length * .85):]


# power of two determining neuron count
n = int(sys.argv[2])

model = Sequential(
    [
        BatchNormalization(),
        Dense(2**n, activation = 'relu', input_shape=(19,)),
        Dense(1, activation = 'sigmoid')
    ]
)

model.compile(
    loss='mse',
    metrics=['mae'],
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
)

history = model.fit(
    train[:,1:],
    train[:,0],
    epochs = int(1e6),
    validation_data = (val[:,1:], val[:,0]),
    verbose = 0
)

print(','.join(history.history['val_mae']))
