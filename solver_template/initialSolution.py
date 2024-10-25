import sys
import misc as m
import random

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

def getBetterInitialSolution(opt: str, evlauation: str, matrix: list[list[float]]):
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
				if evlauation ==  "trivial":
					new_cost = m.calculateCost(new_solution, matrix)
					
					if new_cost < cost:
						solution = new_solution
						cost = new_cost
						improvement = True
						#leave after first improvement
						break 
				elif evlauation == "incremental" and j < len(solution):
					#TODO try to add support for j+1 loop
					cost_difference = m.calculateIncremental(solution, matrix, i, j)
					
					if cost_difference < 0:
						solution = new_solution
						cost += cost_difference
						improvement = True
						break 

	return solution



def getRandomSolution(matrix: list[list[float]]) -> list[int]:
	#list of cities
	list_of_cities = [city for city in range(len(matrix))]
	random.shuffle(list_of_cities)
	return list_of_cities

def nearestInsertion(matrix : list[list[float]]) -> list[int]:
	
	# list of unvisited citites
	unvisited = list(range(len(matrix[0])-1))
	# Random initial city
	initial_city = m.getRandomCity(matrix)
	# Nearest neighbor for the initial city
	nearest_val, nearest_id = m.getNearestNeigh(initial_city, matrix, unvisited)

	# Debug
	# print(f"Initial {initial_city} nearest {nearest_id}")
	
	# Remove the initial tour from unvisited cities
	unvisited.remove(nearest_id)
	#TODO sometimes this throws error dont know why
	#error
	"""
	ValueError: list.remove(x): x not in list
	"""
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
		# print(f"Creating path between: {node} and {min_id}")
		# 
		unvisited.remove(min_id)
		m.insertToTour(tour, pred, min_id)

	return tour

