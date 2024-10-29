import random
import misc as m

def repairMethod(cost, partial_solution, removed_cities, opt, matrix):
	low_opt = opt.lower()
	if low_opt == "random":
		return repairRandom(cost, partial_solution, removed_cities, matrix)
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

		repaired_solution.insert(i+1, city)
	
	return repaired_solution, m.calculateCost(repaired_solution, matrix)

def repairBestAndRandom(cost, partial_solution, removed_cities, matrix):
	# Create a copy of partial_solution to work on
	repaired_solution = partial_solution[:]
	curr_cost = m.calculateCost(repaired_solution, matrix)
	# For each city in deleted_cities, find the best position to insert
	for city in removed_cities:
		if random.random() < 0.2:  # With 20% chance, insert randomly
			#in this case it has to be len-1 because randint includes both boudns
			#meaning for example len=22 could lead to a position 22 which is out of bouds
			best_position = random.randint(0, len(repaired_solution)-1) 
			insert_cost = m.getIncrementalRandom(repaired_solution, matrix, best_position, city)
			curr_cost+=insert_cost
		else:
			best_cost = float('inf')
			best_position = None

			# Loop over each possible position in the tour to insert the city
			for i in range(len(repaired_solution)):
				insert_cost = m.getIncrementalRandom(repaired_solution, matrix, i, city)
				total_cost = insert_cost+curr_cost
				#check if new cost is beneficial
				if total_cost < best_cost:
					best_cost = total_cost
					best_position = i

			curr_cost = best_cost
		
		# Insert the city at the best position found
		repaired_solution.insert(best_position, city)

	return repaired_solution, curr_cost

