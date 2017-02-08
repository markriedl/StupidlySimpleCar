import numpy as np
import tflearn
import sys

# Load CSV file
# For some reason, the CSV must have a single label column. So the dataset has a last dummy column.
from tflearn.data_utils import load_csv
input_data, dummy = load_csv("data.csv", columns_to_ignore=[5, 6, 7, 8])
input_labels, dummy = load_csv("data.csv", columns_to_ignore=[1, 2, 3, 4])

# Put data and labels into a numpy array (matrix)
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

# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=10, show_metric=True)

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
