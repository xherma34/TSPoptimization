import sys
import random
import time

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

def getFarthestDuo(matrix : list[list[float]]):
	max_dist = float('-inf')
	pair = list()
	for i in range(len(matrix)):
		for j in range(i+1, len(matrix)):
			#find the pair with the biggest distance
			if matrix[i][j]>max_dist:
				#get the indexes
				pair = [i,j]
				max_dist = matrix[i][j]
	
	return pair

def getFarthestCityDistance(matrix : list[list[float]], tour: list[int], i:int):
	max_dist = float('-inf')
	for val in tour:
		#find the biggest distance
		if matrix[i][val] > max_dist:
			max_dist = matrix[i][val]

	return max_dist

def getPositionFar(matrix : list[list[float]], tour: list[int], to_add: int):
	best_increase = float('inf')
	position = None
	for x in range(len(tour)):
		pos_b = tour[x]
		pos_a = tour[x+1] if x+1 < len(tour) else tour[0]
		#change in cost after inserting between cities
		new_cost = matrix[pos_b][to_add] + matrix[to_add][pos_a]
		#difference of cost after the insertion
		increase = new_cost - matrix[pos_b][pos_a]
		if increase<best_increase:
			best_increase = increase
			#insert on position after x
			position = x+1 if x+1 < len(tour) else 0
	
	return position


def calculateIncrementalFor2opt(solution: list[int], matrix: list[list[float]], i: int, j: int) -> float:
	#calculate only the part of road that changed
	#cost of original route
	next_j = solution[j+1] if j+1 < len(solution) else solution[0]
	cost_before_swap = matrix[solution[i-1]][solution[i]] + matrix[solution[j]][next_j]
	#swap is from i to j meaning we reverse i and j so the new cost is node before i and node j and node i and after j
	cost_after_swap = matrix[solution[i-1]][solution[j]] + matrix[solution[i]][next_j]

	return cost_after_swap - cost_before_swap


def get2opt(matrix: list[list[float]], solution: list[int], cost: int, max_swaps: int, start_time, timeout):
	swaps = 0
	improvement = True
	while improvement and swaps < max_swaps:
		improvement=False
		for i in range(len(solution)-1):
			for j in range(i+1,len(solution)):
				#you cant revert whole route in 2-opt
				if i==0 and j==len(solution)-1:
					continue
				#calculate what happens if we make the swap in solution
				cost_diff = calculateIncrementalFor2opt(solution, matrix,i,j)
				#if the difference is beneficial make the swap
				if cost + cost_diff < cost:
					#take solution up to i, reverse segment from i to j, take solution from j+1 to the end
					new_solution = solution[:i] + list(reversed(solution[i:j+1])) + solution[j+1:]
					solution = new_solution
					cost += cost_diff
					improvement = True
					swaps+=1
					#leave after first improvement
					break 
			#first improvement
			if improvement:
				break
		if time.time()-start_time >= timeout:
			return solution, cost
	return solution, cost

def getIncrementalRandom(solution: list[int], matrix: list[list[float]], best_position: int, city: int) -> float:
	#to get the change of cost after insert i need indexes before and current
	before = solution[best_position-1] if best_position>0 else solution[-1]
	after = solution[best_position] if best_position<len(solution) else solution[0]
	#we need to calculate the cost which is created by inserting between before and after
	cost = matrix[before][city] + matrix[city][after]
	#also have to subtract the original cost
	increase_cost = cost - matrix[before][after]
	
	return increase_cost

def getCostOfSequence(prev, current, next, matrix):
	cost_decrease = 0
	cost_decrease += matrix[prev][current]
	cost_decrease += matrix[current][next]
	return cost_decrease

def getCostOfNeighbours(prev, next, matrix):
	return matrix[prev][next]