import misc as m

def increaseDestroySize(curr_size, curr_perc, tour_size):

	# Increase by 5 percent
	new_perc = curr_perc + 5
	# threshold is 50 percent
	if new_perc > 50:
		new_perc = 50
	# increase the size
	new_size  = int(tour_size * (new_perc / 100))

	print(f"stagnation, increasing the destroy size from {curr_size} to {new_size}")
	print(f"stagnation, increasing the destroy size PERC from {curr_perc} to {new_perc}")
	return new_size, new_perc
	
	
def decreaseDestroySize(curr_size, curr_perc, tour_size):

	# Decrease by 5 percent
	new_perc = curr_perc - 5
	# threshold is 50 percent
	if new_perc < 15:
		new_perc = 15
	# increase the size
	new_size  = int(tour_size * (new_perc / 100))

	print(f"stagnation, increasing the destroy size from {curr_size} to {new_size}")
	print(f"stagnation, increasing the destroy size PERC from {curr_perc} to {new_perc}")
	return new_size, new_perc

	

def adaptiveRepairAndDestroy(tour : list[int], matrix : list[list[float]], max_iterations : int):
	# Setup counter for no improvements
	stag_runs_cnt = 0
	# Setup a threshold for how many iterations without improvement are okay
	threshold = 5
	# Calculate current cost of the tour
	best_cost = m.calculateCost(tour, matrix)
	# Set initial tour to best tour
	best_tour = tour[:]
	# Save the number of elements in complete tour
	tour_len = len(tour)
	
	# Parameters for destroy and repair
	repair_method = "greedy"
	# Calculate as  percentage of the len(tour) typed into integer
	destroy_size_perc = 15
	destroy_size  = int(len(tour) * (destroy_size_perc / 100))

	print(f"initial destroy size {destroy_size} with percentage of {destroy_size_perc}")

	# Main loop
	for iterations in range(max_iterations):
		# Check if improvement is stagnating => iterations without improvement > threshold do:
		if stag_runs_cnt > threshold:
			destroy_size, destroy_size_perc = increaseDestroySize(destroy_size, destroy_size_perc, tour_len)
			# DEBUG -> REMOVE
			print(f"destroy size back in the function: {destroy_size} destroy percentage back in function {destroy_size_perc}")
			repair_method = "diverse"
			# DEBUG -> REMOVE
			stag_runs_cnt = 0
		else:
			# print(f"no stagnation, increasing the destroy size")
			# decreaseDestroySize(destroy_size, destroy_size_perc, tour_len)
			repair_method = "greedy"
		
		# Do destroy(tour, city_cnt) -> partial_tour, removedCities
		# Do repair(partial_tour, removed_cities, matrix, repair_strategy) -> repaired_tour

		stag_runs_cnt += 1
		# Calculate new_cost = cost(repaired_tour)
		# if new_cost < best_cost
			# best_tour = repaired_tour
			# best_cost = new_cost
			# improvement counter = 0
		# else
			# improvement counter ++
		
		# if timeout
			# break
	return 6
	# return best_tour, best_cost


