import sys
import random

# Return minimal value and minimal index
def getNearestNeigh(node : int, matrix):

	# Check if node isnt out of bounds of matrix
	if node < 0 or node >= len(matrix):
		raise IndexError(f"Node index {node} is out of range for matrix size {len(matrix)}")

	return min((val, idx) for idx, val in enumerate(matrix[node]) if idx != node)

# Retruns random index from the matrix
def getRandomCity(matrix):
	return random.randint(0, len(matrix[0])-1)

# Returns: node, shortest node to node, the path distance
def getShortestPath(tour, matrix):
	# variables
	global_min = float('inf')
	global_min_id = 0
	node_id = 0

	# TODO do this in the initialSolution.py so u dont need to loop through it every time -> saves time
	updated_matrix = setMatrixValueOn(matrix, tour, float('inf'))

	for x in tour:
		min_val, min_id = getNearestNeigh(x, updated_matrix)

		if(min_val < global_min):
			global_min = min_val
			global_min_id = min_id
			node_id = x

	return node_id, global_min_id, global_min

# Calculates cost of a solutions and returns the cost value
def calculateCost(solution, matrix) -> float:
    cost = 0
    for i in solution:
        # Dont get out of bounds
        if i+1 < len(solution):
            cost += matrix[i][i+1]
    return cost

def insertToPath(tour, node_from, node_to):
	index = tour.index(node_from)
	tour.insert(index+1, node_to)

def setMatrixValueOn(matrix, indexes, value):
	new_matrix = [row[:] for row in matrix]
	for i in range(len(indexes) - 1):
		for j in range(i + 1, len(indexes)):
			new_matrix[indexes[i]][indexes[j]] = value
			new_matrix[indexes[j]][indexes[i]] = value
			
	return new_matrix
