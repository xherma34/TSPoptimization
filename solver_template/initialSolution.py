import sys
import misc as m
import random
import time

def getInitialSolution(opt : str, matrix : list[list[float]]) -> list:
	optLow = opt.lower()
	if optLow == "nearest":
		return nearestInsertion(matrix)
	# elif optLow == "farthest":
	# 	return farthestInsertion(matrix)
	elif optLow == "random":
		return getRandomSolution(matrix)
	else:
		raise Exception("Error: undefined option in initialSolution.py:getInitialSolution()")

def getBetterInitialSolution(opt: str, matrix: list[list[float]]):
	#2-opt
	solution = getInitialSolution(opt, matrix)
	cost = m.calculateCost(solution, matrix)

	improvement = True	
	while improvement:
		improvement=False
		for i in range(len(solution)-1):
			for j in range(i+1,len(solution)+1):#+1 beacuse of the way python slices indexes this ensures that last index will also be part of swaping
				#take solution up to i, reverse segment from i up to j, take solution from j to the end
				new_solution = solution[:i] + list(reversed(solution[i:j])) + solution[j:]
				new_cost = m.calculateCost(new_solution, matrix)
				
				if new_cost < cost:
					solution = new_solution
					cost = new_cost
					improvement = True
	return solution

def getRandomSolution(matrix: list[list[float]]) -> list[int]:
	#list of cities
	list_of_cities = [city for city in range(len(matrix))]
	random.shuffle(list_of_cities)
	return list_of_cities

#TODO -> refactor to take in list of elements and unvisited list and do it from that
def nearestInsertion(matrix : list[list[float]]) -> list[int]:
	
	start_time = time.time()
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
				node = x
		# Find the best position in current solution
		pred = m.findBestPosition(tour, min_id, matrix)
		# DEBUG
		# print(f"Creating path between: {node} and {min_id}")
		# 
		if time.time() - start_time >= 60:
			print(f"Time out after one minute, number of inserted {len(tour)}, total number {len()}")
			break
		unvisited.remove(min_id)
		m.insertToTour(tour, pred, min_id)

	return tour

