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

	for i in solution:
		# Dont get out of bounds
		if i+1 < len(solution):
			cost += matrix[i][i+1]
	
	cost += matrix[solution[0]][solution[len(solution)-1]]
	return cost
	
# Returns index in tour after which to add the closest_node
def findBestPosition(tour : list[int], closest_node : int, matrix : list[list[float]]) -> int:
	pred = float('inf')
	pred_val = float('inf')
	
	for x in tour:
		val = matrix[x][closest_node]
		if val < pred_val:
			val = pred_val
			pred = x
	
	return pred

# Inserts node_new after node in list tour
def insertToTour(tour : list[int], node : int, new_node : int):
	index = tour.index(node)
	tour.insert(index+1, new_node)



# When you insert something in the list, update cost