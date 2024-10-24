import sys
import misc as m

def getInitialSolution(opt : str, matrix : list[list[float]]):

	optLow = opt.lower()
	if optLow == "nearest":
		return nearestInsertion(matrix)
	# elif optLow == "farthest":
	# 	return farthestInsertion(matrix)
	elif optLow == "random":
		return 2
	else:
		raise Exception("Error: undefined option in initialSolution.py:getInitialSolution()")

def nearestInsertion(matrix : list[list[float]]) -> list[int]:
	
	# list of unvisited citites
	unvisited = list(range(len(matrix[0])-1))
	# Random initial city
	initial_city = m.getRandomCity(matrix)
	# Nearest neighbor for the initial city
	nearest_val, nearest_id = m.getNearestNeigh(initial_city, matrix, unvisited)

	# Debug
	print(f"Initial {initial_city} nearest {nearest_id}")
	
	# Remove the initial tour from unvisited cities
	unvisited.remove(nearest_id)
	unvisited.remove(initial_city)

	# Debug
	# print(f"Unvisited after insertion: {unvisited}")

	# Initial tour
	tour = [initial_city, nearest_id]
	# TODO cost

	while len(unvisited) != 0:
		# Set bounds for finding minimum
		min_val = float('inf')
		min_id = float('inf')
		# get shortest possible path for current tour
		for x in tour:
			# get nearest neighbour
			val, id = m.getNearestNeigh(x, matrix, unvisited)
			# Update variables if shortest path for current tour was found
			if val < min_val:
				min_val = val
				min_id = id
				node = x
		# Find the best position in current solution
		pred = m.findBestPosition(tour, min_id, matrix)
		# DEBUG
		print(f"Creating path between: {node} and {min_id}")
		# 
		unvisited.remove(min_id)
		m.insertToTour(tour, pred, min_id)

	return tour

