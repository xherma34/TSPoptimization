import misc as m
import random
import math

def increaseDestroySize(curr_size, curr_perc, tour_size):

	# Increase by 5 percent
	new_perc = curr_perc + 5
	# threshold is 50 percent
	if new_perc > 50:
		new_perc = 50
	# increase the size
	new_size  = int(tour_size * (new_perc / 100))

	# print(f"stagnation, increasing the destroy size from {curr_size} to {new_size}")
	# print(f"stagnation, increasing the destroy size PERC from {curr_perc} to {new_perc}")
	return new_size, new_perc
	
	
def decreaseDestroySize(curr_size, curr_perc, tour_size):
	# Decrease by 5 percent
	new_perc = curr_perc - 5
	# threshold is 50 percent
	if new_perc < 15:
		new_perc = 15
	# increase the size
	new_size  = int(tour_size * (new_perc / 100))

	# print(f"stagnation, increasing the destroy size from {curr_size} to {new_size}")
	# print(f"stagnation, increasing the destroy size PERC from {curr_perc} to {new_perc}")
	return new_size, new_perc

# TODO -> maybe instead of list use dictionary so we dont need to look for costs all the time
def destroyMethod(tour : list[int], num_of_cities : int, opt : str, matrix):
	opt_low = opt.lower()
	if opt_low == "random":
		return destroyRandom(tour, num_of_cities)
	elif opt_low == "highestcost":
		return destroyHighestCost(tour, num_of_cities, matrix)
	else:
		return destroyRandom(tour, num_of_cities)

def destroyRandom(tour : list[int], num_of_cities : int):
	# Randomly select cities to delete from the tour
	deleted_cities = random.sample(tour, num_of_cities)
	# Create partial_tour by removing the selected cities from the original tour
	partial_tour = [city for city in tour if city not in deleted_cities]
	print(f"----------- Entering random -----------")
	print(f"Extracted cities: {deleted_cities}")
	
	return partial_tour, deleted_cities

# Removes the num_of_cities with highest cost
def destroyHighestCost(tour : list[int], num_of_cities : int, matrix : list[list[float]]):
	# Create dictionary [City, Cost to next city]
	tour_dict = {}
	for city in tour:
		# Dont get out of bounds
		if city+1 < len(tour):
			tour_dict[city] = matrix[city][city+1]
	# Add the cyclic path
	tour_dict[len(tour)-1] = matrix[tour[0]][len(tour)-1]
	# Sort in descending order
	sorted_dict = sorted(tour_dict.items(), key= lambda item: item[1], reverse= True)
	# print(f"SORTED DICTIONARY: {sorted_dict}")
	# Take first num_of_cities of the sorted path list
	removed_cities = [item[0] for item in sorted_dict][:num_of_cities]
	# Create the partial tour by trimming out the removed cities
	partial_tour = [city for city in tour if city not in removed_cities]
	
	# DEBUG
	# print(f"----------- Entering highest cost destroy -----------")
	# print(f"Dictionary of costs: {tour_dict}")
	# print(f"After sort: {sorted_dict}")
	# print(f"Extracted cities: {removed_cities}")

	return partial_tour, removed_cities

def repairMethod(partial_solution, removed_cities, opt, matrix):
	low_opt = opt.lower()
	if low_opt == "random":
		return repairRandom(partial_solution, removed_cities, matrix)
	elif low_opt == "bestposition":
		return m.nearestInsertionRefac(partial_solution, removed_cities, matrix)
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

# TODO -> FIX: somehow even when changing the destroy method to clusters
def adaptiveRepairAndDestroy(tour : list[int], matrix : list[list[float]], max_iterations : int):
	# Setup counter for stagnation
	stag_runs_cnt = 0
	# Setup a threshold for how many iterations without improvement are okay
	threshold = 10
	# Calculate current cost of the tour
	best_cost = m.calculateCost(tour, matrix)
	# Make a copy of initial tour and store it to best_tour
	best_tour = tour[:]
	# Save the number of elements in complete tour
	tour_len = len(tour)
	
	# Parameters for destroy and repair
	destroy_method = "highestcost"
	repair_method = "bestposition"
	# Calculate as  percentage of the len(tour) casted into integer
	destroy_size_perc = 30
	destroy_size  = int(len(tour) * (destroy_size_perc / 100))
	stag_cnt = 0

	# Main loop
	for iteration in range(max_iterations):
		# if stagnation
		if stag_runs_cnt > threshold:
			# If stagnation happens, change the destroy and repair methods to be more aggresive
			# DESTROY -> bigger number of deleted cities
			# DESTROY_METHOD,  -> something that will take me out of the local optima
			stag_cnt += 1
			# print(f"Stagnation after {iterations} iterations")
			# Increase destruction rate
			destroy_size, destroy_size_perc = increaseDestroySize(destroy_size, destroy_size_perc, tour_len)
		# 	repair_method = "diverse"
		# 	# Use a method for destroy which: Escapes the local optima -> 
		# 	# either bring randomness or eliminate clusters of nodes (randomly)
		# 	destroy_method = "random"

		partial_solution, removed_cities = destroyCluster(best_tour, destroy_size, matrix)

		# if stag_cnt > 20: 
		# 	partial_solution, removed_cities = destroyCluster(best_tour, destroy_size, matrix)
		# else:
		# 	partial_solution, removed_cities = destroy(best_tour, destroy_size, matrix)
		repaired_tour, repaired_cost = repair(partial_solution, removed_cities, matrix)
		# print(f"Iteration: {iteration}")
		# print(f"Partial solution: {partial_solution}")
		# print(f"Removed cities: {removed_cities}")
		# print(f"Repaired tour: {repaired_tour}")
		# print(f"Repaired cost: {repaired_cost}")
		# print(f"Best cost: {best_cost}")
		# print(f"Stagnation counter: {stag_runs_cnt}")
		# print(f"Destroy size: {destroy_size}\n\n")
		

		# TODO -> move into function
		# print("------------------------------------------------------")
		if repaired_cost < best_cost:
			# print("HOVNO")
			# print(f"Cost adjusted: current best tour: \n{best_tour}\nwith cost {best_cost}\n\n")
			# print(f"Repaired tour: \n{repaired_tour} \nwith cost: {repaired_cost}")
			best_tour = repaired_tour
			best_cost = repaired_cost
			stag_runs_cnt = 0
		else:
			stag_runs_cnt += 1
			# print(f"Cost not adjusted: current best tour: \n{best_tour}\nwith cost {best_cost}")
			# print(f"Repaired tour: \n{repaired_tour}\nwith cost: {repaired_cost}")
		# else
			# TODO -> maybe if we struggle we can do simmulated annealing to not get stuck on local optima
			# SIMMULATED ANNEALING:
				# if random < acceptance_prob
					# accept new solution
				# else  		 
					# stagnation counter ++
		# temperature += cooling_rate
		# 
	return best_tour, best_cost


def destroy(tour, destroy_size, matrix):
	# Create a copy of the tour
	partial_solution = tour[:]
	deleted_cities = []
	
	# Identify the worst paths by calculating costs of each segment in the tour
	# (since it’s cyclic, include the last-to-first segment)
	path_costs = []
	for i in range(len(tour)):
		next_city = tour[(i + 1) % len(tour)]
		cost = matrix[tour[i]][next_city]
		path_costs.append((cost, tour[i]))
	
	# Sort the paths by cost in descending order (to remove the worst paths)
	path_costs.sort(reverse=True, key=lambda x: x[0])
	
	# Select the top 'num_of_cities' worst paths to remove
	cities_to_remove = [city for _, city in path_costs[:destroy_size]]
	
	# Add some randomness: randomly select some additional cities to remove
	while len(cities_to_remove) < destroy_size:
		random_city = random.choice(tour)
		if random_city not in cities_to_remove:
			cities_to_remove.append(random_city)
	
	# Remove the selected cities from the partial solution
	for city in cities_to_remove:
		deleted_cities.append(city)
		partial_solution.remove(city)
	
	return partial_solution, deleted_cities

def destroyCluster(tour, num_of_cities, matrix):
    # Create a copy of the tour to work on
    partial_solution = tour[:]
    deleted_cities = []

    # Select a random city to start the cluster removal
    cluster_start = random.randint(0, len(tour) - 1)
    
    # Remove a contiguous block of cities (cluster)
    for i in range(num_of_cities):
        # Calculate the index of the city to remove (wrap around the tour)
        city_index = (cluster_start + i) % len(partial_solution)
        city = partial_solution[city_index]
        
        # Add the city to the list of deleted cities and remove from the tour
        deleted_cities.append(city)
    
    # Remove the cities in the cluster from the partial_solution
    for city in deleted_cities:
        partial_solution.remove(city)
    
    return partial_solution, deleted_cities


def repair(partial_solution, deleted_cities, matrix):
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
                cost = m.getCost(temp_tour, matrix)
                
                if cost < best_cost:
                    best_cost = cost
                    best_position = i
        
        # Insert the city at the best position found
        tour.insert(best_position, city)
    
    return tour