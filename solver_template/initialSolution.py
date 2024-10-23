import sys
import misc as m

def getInitialSolution(opt, matrix):

	optLow = opt.lower()
	if optLow == "farthest":
		return farthestInsertion(matrix)
	elif optLow == "nearest":
		return nearestInsertion(matrix)
	elif optLow == "random":
		return 2
	else:
		raise Exception("Error: undefined option in initialSolution.py:getInitialSolution()")

def nearestInsertion(matrix):
	initial_city = m.getRandomCity(matrix)
	val, nearest_city = m.getNearestNeigh(initial_city, matrix)

	print("for city "+ str(initial_city) + " Closest neighbor is: " + str(nearest_city) + " with distance: " + str(val))

	path = [initial_city, nearest_city]

	m.getShortestPath(path, matrix)

	while len(path) != len(matrix[0]):
		node, new_node, val = m.getShortestPath(path, matrix)
		m.insertToPath(path, node, new_node)
		
		print("Adding: " + str(new_node) + " after: " + str(node) + " with distance: " + str(val))

	return path



def farthestInsertion(matrix):
	# Step 1: Start with the initial tour containing 2 cities
	initial_city = m.getRandomCity(matrix)
	nearest_city = m.getNearestNeigh(nearest_city, matrix)
	path = [initial_city, nearest_city]
	# Step 2: While there are cities not in the Tour
	while len(path) != len(matrix[0]):
		break
		# Step 3: Find the city farthest from any city in the current Tour
        # FarthestCity = find_farthest_city(Tour, matrix)
        # Step 4: Insert the farthest city into the best position in the Tour
        
    
    # Step 5: Return the completed tour
