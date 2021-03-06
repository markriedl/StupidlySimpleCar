from __future__ import print_function

import numpy as np
import tflearn
import copy, sys

# Handle command line arguments
loadModel = False # Is the user requesting to use a pre-trained model?
modelname = '' # If so, what is the name of that model filename?
filename = '' # If data is being loaded from a CSV instead, this is the filename
filehead = '' # And this is the part of the filename before the .csv

if len(sys.argv) < 2:
	# Invalid command line usage
	print("usage: python "+sys.argv[0]+" file.csv")
	print("usage: python "+sys.argv[0]+" -m model.tflearn")
	exit()
elif len(sys.argv) >= 3 and sys.argv[1] == '-m':
	# User wants to load a model
	modelname = sys.argv[2]
	loadModel = True
else:
	# Default: user wants to load data from a CSV
	filename = sys.argv[1]
	filehead = filename.split('.')[0]

# Some initializations
input_data = None # All the data from the CSV will be held here (including supervision labels)
input_labels = None # All the supervision labels from the CSV will be held here
data = None # Data for training
labels = None # supervision labels

# Read the CSV
if not loadModel:
	# Load CSV file
	# For some reason, the CSV must have a single label column. So the dataset has a last dummy column.
	from tflearn.data_utils import load_csv
	input_data, dummy = load_csv(filename, columns_to_ignore=[5, 6, 7, 8])
	input_labels, dummy = load_csv(filename, columns_to_ignore=[1, 2, 3, 4])

	# Put data and labels into a numpy array (matrix)
	#data = preprocess(input_data, num_columns, data_columns)
	#labels = preprocess(input_labels, num_columns, label_columns)
	data = np.array(input_data, dtype=np.float32)
	labels = np.array(input_labels, dtype=np.float32)

# Build neural network
net = tflearn.input_data(shape=[None, 4]) # 4 inputs
net = tflearn.fully_connected(net, 16, activation='relu') # hidden layer of 16 nodes
net = tflearn.fully_connected(net, 16, activation='relu') # hidden layer of 16 nodes
net = tflearn.fully_connected(net, 4, activation='relu') # 4 outputs
net = tflearn.regression(net, loss='mean_square')

# Define model
model = tflearn.DNN(net)

# Load or train?
if loadModel:
	# Load the model
	model.load(modelname)
else:
	# Start training (apply gradient descent algorithm)
	model.fit(data, labels, n_epoch=10, show_metric=True)
	# Save the model
	model.save(filehead+'.tflearn')

# User testing loop
while True:
	# Ask the user for values (0.0 - 1.0) for each sensor
	print("front proximity?")
	f = sys.stdin.readline()
	print("rear proximity?")
	b = sys.stdin.readline()
	print("left proximity?")
	l = sys.stdin.readline()
	print("right proximity?")
	r = sys.stdin.readline()

	# Make prediction
	test = [[f, b, l, r]] # test input
	pred = model.predict(test) # run test input through neural net
	# Report
	print("Prediction: ")
	print("brakes: "+str(pred[0][0]))
	print("accelerator: "+str(pred[0][1]))
	print("steer left: "+str(pred[0][2]))
	print("steer right: "+str(pred[0][3]))
	print("--")
