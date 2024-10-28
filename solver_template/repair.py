import random
import misc as m

def repairMethod(cost, partial_solution, removed_cities, opt, matrix):
	low_opt = opt.lower()
	if low_opt == "random":
		return repairRandom(cost, partial_solution, removed_cities, matrix)
	# TODO -> implement
	# elif low_opt == "bestposition":
	# 	pass
		# return nearestInsertionRefac(partial_solution, removed_cities, matrix)
	elif low_opt == "bestrandom":
		return repairBestAndRandom(cost, partial_solution, removed_cities, matrix)
	else:
		return repairRandom(cost, partial_solution, removed_cities, matrix)

def repairRandom(cost, partial_solution, removed_cities, matrix):
	# Create copy
	repaired_solution = partial_solution[:]
	# Get list of random indeces from partial solution (number of indeces = len(removed_cities))
	append_after = random.sample(partial_solution, len(removed_cities))

	# cost_update = 0
	for city, after in zip(removed_cities, append_after):
		i = repaired_solution.index(after)

		# # Incremental cost update
		# prev = after
		# next = repaired_solution[(i+1)%len(repaired_solution)]

		# cost_update -= matrix[prev][next]
		# cost_update += matrix[prev][city] + matrix[city][next]

		repaired_solution.insert(i+1, city)
	
	return repaired_solution, m.calculateCost(repaired_solution, matrix)

def repairBestAndRandom(cost, partial_solution, removed_cities, matrix):
	# Create a copy of partial_solution to work on
	repaired_solution = partial_solution[:]
	
	# For each city in deleted_cities, find the best position to insert
	for city in removed_cities:
		if random.random() < 0.2:  # With 20% chance, insert randomly
			best_position = random.randint(0, len(repaired_solution))
		else:
			best_cost = float('inf')
			best_position = None

			# Loop over each possible position in the tour to insert the city
			for i in range(len(repaired_solution) + 1):
				# Create a temporary tour with the city inserted at position i
				temp_tour = repaired_solution[:i] + [city] + repaired_solution[i:]
				
				# Calculate the cost of the temporary tour
				cost = m.calculateCost(temp_tour, matrix)
				
				if cost < best_cost:
					best_cost = cost
					best_position = i
		
		# Insert the city at the best position found
		repaired_solution.insert(best_position, city)
	
	return repaired_solution, m.calculateCost(repaired_solution, matrix)

