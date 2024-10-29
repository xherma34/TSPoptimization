import sys
import misc as m
import random
import time

def getInitialSolution(opt : str, matrix : list[list[float]]) -> list:
	optLow = opt.lower()
	if optLow == "nearest": #this is probably a better initial solution
		return nearestInsertion(matrix)
	elif optLow == "farthest":
		return farthestInsertion(matrix)
	elif optLow == "random": #trivial initial solution
		return getRandomSolution(matrix)
	else:
		raise Exception("Error: undefined option in initialSolution.py:getInitialSolution()")


def getRandomSolution(matrix: list[list[float]]) -> list[int]:
	list_of_cities = [city for city in range(len(matrix))]
	random.shuffle(list_of_cities)
	return list_of_cities


def nearestInsertion(matrix : list[list[float]]) -> list[int]:
	
	# list of unvisited citites
	unvisited = list(range(len(matrix[0])))
	# Random initial city
	initial_city = m.getRandomCity(matrix)

	assert initial_city in unvisited, f"Error: the value {initial_city} is not in {unvisited}"

	# Nearest neighbor for the initial city
	nearest_val, nearest_id = m.getNearestNeigh(initial_city, matrix, unvisited)
	
	# Remove the initial tour from unvisited cities
	unvisited.remove(nearest_id)
	unvisited.remove(initial_city)

	# Initial tour
	tour = [initial_city, nearest_id]

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
		# Find the best position in current solution
		pred = m.findBestPosition(tour, min_id, matrix)
		unvisited.remove(min_id)
		m.insertToTour(tour, pred, min_id)

	return tour


def farthestInsertion(matrix : list[list[float]]) -> list[int]:
	# get the cities with biggest distance
	tour = m.getFarthestDuo(matrix)
	#until the tour recieves all nodes from matrix
	while len(tour) != len(matrix):
		max_distane = float('-inf')
		to_add = None
		for i in range(len(matrix)):
			if i not in tour:
				#get the distance of a city
				distance =  m.getFarthestCityDistance(matrix, tour, i)
				if distance > max_distane:
					max_distane = distance
					#get the city with the biggest distance
					to_add = i
		#find the position with smallest increase
		position = m.getPositionFar(matrix, tour, to_add)
		tour.insert(position, to_add)

	return tour