import sys
import random

# Return minimal value and minimal index
def getNearestNeigh(node : int, matrix : list[list[float]], unvisited : list[int]) -> tuple[float, int]:

	min_id = 0
	min_val = float('inf')
	
	for x in range(len(matrix[node])):
		if matrix[node][x] < min_val and x in unvisited and x != node:
			min_id = x
			min_val = matrix[node][x]
	
	return min_val, min_id

# Retruns random index from the matrix
def getRandomCity(matrix : list[list[float]]) -> int:
	return random.randint(0, len(matrix[0])-1)

# Calculates cost of a solutions and returns the cost value
def calculateCost(solution : list[int], matrix : list[list[float]]) -> float:
	cost = 0
	for i in range(len(solution)-1):
		cost += matrix[solution[i]][solution[i + 1]]

	# Add the cyclic path between first and last city
	cost+=matrix[solution[-1]][solution[0]]
	return cost

def calculateIncremental(solution: list[int], matrix: list[list[float]], i: int, j: int) -> float:
	#TODO implement after destroy and repair
	pass

# Returns index in tour after which to add the closest_node
def findBestPosition(tour : list[int], closest_node : int, matrix : list[list[float]]) -> int:
	insert_after = 0
	best_cost = float('inf')
	for city in tour:
		mod_tour = tour[:]
		mod_tour.insert(city+1, closest_node)
		curr_cost = calculateCost(mod_tour, matrix)
		if curr_cost < best_cost:
			insert_after = city
	return insert_after

# Inserts node_new after node in list tour
def insertToTour(tour : list[int], node : int, new_node : int):
	index = tour.index(node)
	tour.insert(index+1, new_node)



# When you insert something in the list, update cost

def get2opt(matrix: list[list[float]], solution: list[int], cost: int, max_swaps: int):
	swaps = 0
	improvement = True
	while improvement and swaps < max_swaps:
		improvement=False
		for i in range(len(solution)-1):
			for j in range(i+1,len(solution)+1):#+1 beacuse of the way python slices indexes this ensures that last index will also be part of swaping
				#take solution up to i, reverse segment from i up to j, take solution from j to the end
				new_solution = solution[:i] + list(reversed(solution[i:j])) + solution[j:]
				new_cost = calculateCost(new_solution, matrix)
					
				if new_cost < cost:
					solution = new_solution
					cost = new_cost
					improvement = True
					swaps+=1
					#leave after first improvement
					break 
			if improvement:
				break

	return solution, cost

def getFarthest(matrix : list[list[float]]):
	max_dist = float('-inf')
	pair = list()
	for i in range(len(matrix)):
		for j in range(i+1, len(matrix)):
			if matrix[i][j]>max_dist:
				pair = [i,j] #get the indexes of cities
				max_dist = matrix[i][j]
	
	print(max_dist)
	return pair