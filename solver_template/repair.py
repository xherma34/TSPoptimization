import random
import misc as m

def repairMethod(partial_solution, removed_cities, opt, matrix):
	low_opt = opt.lower()
	if low_opt == "random":
		return repairRandom(partial_solution, removed_cities, matrix)
	# TODO -> implement
	# elif low_opt == "bestposition":
	# 	pass
		# return nearestInsertionRefac(partial_solution, removed_cities, matrix)
	elif low_opt == "bestrandom":
		return repairBestAndRandom(partial_solution, removed_cities, matrix)
	else:
		return repairRandom(partial_solution, removed_cities, matrix)

def repairRandom(partial_solution, removed_cities, matrix):
	# Create copy
	repaired_solution = partial_solution[:]
	# Get list of random indeces from partial solution (number of indeces = len(removed_cities))
	predecesors = random.sample(partial_solution, len(removed_cities))
	for removed, i in zip(removed_cities, predecesors):
		m.insertToTour(repaired_solution, i, removed)
	# Add the removed_cities respectively after the indexes
	
	return repaired_solution, m.calculateCost(repaired_solution, matrix)

def repairBestAndRandom(partial_solution, deleted_cities, matrix):
	# Create a copy of partial_solution to work on
	tour = partial_solution[:]
	
	# For each city in deleted_cities, find the best position to insert
	for city in deleted_cities:
		if random.random() < 0.2:  # With 20% chance, insert randomly
			best_position = random.randint(0, len(tour))
		else:
			best_cost = float('inf')
			best_position = None

			# Loop over each possible position in the tour to insert the city
			for i in range(len(tour) + 1):
				# Create a temporary tour with the city inserted at position i
				temp_tour = tour[:i] + [city] + tour[i:]
				
				# Calculate the cost of the temporary tour
				cost = m.calculateCost(temp_tour, matrix)
				
				if cost < best_cost:
					best_cost = cost
					best_position = i
		
		# Insert the city at the best position found
		tour.insert(best_position, city)
	
	return tour, m.calculateCost(tour, matrix)