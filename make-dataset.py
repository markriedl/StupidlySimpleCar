import random, sys

verbose = False

filename = '' # If data is being loaded from a CSV instead, this is the filename
numRows = 0 # How many samples?

if len(sys.argv) < 3:
	# Invalid command line usage
	print("usage: python "+sys.argv[0]+" output.csv num_samples")
	exit()
else:
	filename = sys.argv[1]
	numRows = int(sys.argv[2])

# Open the file
with open(filename, 'w') as file:

	#write the header row
	file.write('front,back,left,right,brakes,accel,left,right,dummy\n')
	
	# Make new rows
	for n in range(numRows):

		# Generate a random state
		# the distance to the nearest car in front/back/left/right is normalized from 0.0 (closest) to 1.0 (farthest)
		carInFrontDist = random.random()
		carInBackDist = random.random()
		carLeftDist = random.random()
		carRightDist = random.random()

		# Response to the state. 1 =  brakes/accelerator/steer-left/steer-right is activated. 0=not activated
		# Though binary, we will be using numbers
		brakes = 0.0
		accel = 1.0
		left = 0.0
		right = 0.0
		
		# Should I accelerate or brake?
		if carInFrontDist < 0.50:
			# Car is close, brake
			# Unless there is another car close behind
			if carInBackDist > 0.50:
				# Okay to brake
				brakes = 1.0 - (carInFrontDist/0.50)
				accel = 0
			else:
				# Not okay to brake, but at least stop accelerating
				brakes = 0
				accel = 0
		else:
			# Car in front is not close, continue to accelerate
			accel = (carInFrontDist - 0.50)/0.50
			brakes = 0
		
		# Should I turn left or right? (can't do both)
		if carLeftDist < 0.50 and carRightDist > 0.50:
			# A car is close on the left, there is space on the right
			right = 1.0 - (carLeftDist/0.50)
			left = 0
		elif carRightDist < 0.50 and carLeftDist > 0.50:
			# A car is close on the right, there is space on the left
			left = 1.0 - (carRightDist/0.50)
			right = 0
		
		# Coma separated row of data
		out = str(carInFrontDist)+','+str(carInBackDist)+','+str(carLeftDist)+','+str(carRightDist)+','+str(brakes)+','+str(accel)+','+str(left)+','+str(right)+',0'
		
		# Maybe print to screen too?
		if verbose:
			print out
		
		# Write to file
		file.write(out+'\n')

