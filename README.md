- **data:** Directory containing all the subdirectories of groundtruthed/reduced data on which the model is trained/validated/tested.


- **results:** Folder containing error logs and results from running model.py to test the neuron counts for neural nets to predict Starts/Ends. csv files countain training and validation mean absolute error at each point in the training process.


- **model.ipynb:** Notebook used to write and test the model.


- **simulation.ipynb:** Notebook used to write and test the simulation of the model on "real" data.


- **model.py:** Python script to train the model, given some training data. Neuron counts for the hidden layer, and model type (Start or End) can be specified via the command line. The script first loops through all the data-containing files of the data directory, adds all their contents (temperature readings and labels) to a big dataframe, and randomly chooses contiguous sets of temperature readings, half of which have the middle value assigned the relevant label, and half of which do not. Sets of data for which the middle value has the label are paired with the target value 1, and sets which do not are paired with target value 0. This data is then randomly shuffled, and broken up into training/testing/validation sets. Finally, the model is compiled and trained to predict the target. This script can also be used to save the weights of a trained model.


- **script.sh:** Script to conveniently run model.py with a range of desired neuron counts/model types.
