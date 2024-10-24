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

	for city in solution:
		# Dont get out of bounds
		if city+1 < len(solution):
			cost += matrix[city][city+1]
	
	# Add the cyclic path between first and last city
	cost += matrix[solution[0]][solution[len(solution)-1]]
	return cost
	
# Returns index in tour after which to add the closest_node
def findBestPosition(tour : list[int], closest_node : int, matrix : list[list[float]]) -> int:
	insert_after = 0
	best_cost = float('inf')
	
	# calculate the distance of: C-A-B A-C-B A-B-C
	# Loop through the whole tour (tour: A-B), closest_node = C
		# Calculate cost and save it
		# Save the index of current i
		# if cost < best_cost
			# best_cost = cost
			# best_pos = i

	
	# Input tour: A-B, closest_node: C
	# calculate the distance of: A-C-B-A A-B-C-A, whichever has lowest cost, return that 
	# Loop throgh the whole tour
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