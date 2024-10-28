import random
import misc as m

# TODO -> decrease cost when removing cities

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

def destroyMethod(tour : list[int], num_of_cities : int, opt : str, matrix, cost : int):
	opt_low = opt.lower()
	if opt_low == "random":
		return destroyRandom(tour, num_of_cities, matrix, cost)
	elif opt_low == "highestcost":
		return destroyHighestCost(tour, num_of_cities, matrix, cost)
	elif opt_low == "cluster":
		return destroyCluster(tour, num_of_cities, matrix, cost)
	elif opt_low == "highestrandom":
		return destroyHighestRandom(tour, num_of_cities, matrix, cost)
	else:
		return destroyRandom(tour, num_of_cities)

def destroyHighestRandom(tour, destroy_size, matrix, cost):
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
	print(f"LENGTH {len(partial_solution)}")
	new_cost = getCostUpdate(tour, cities_to_remove, cost, matrix)

	return partial_solution, deleted_cities, new_cost

# TODO -> implement adaptive cost update
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

def destroyRandom(tour : list[int], num_of_cities : int, matrix : list[list[float]], cost : int):
	# print(f"Cost for tour before destroy: {m.calculateCost(tour, matrix)}")
	# Randomly select cities to delete from the tour
	removed_cities = random.sample(tour, num_of_cities)
	# Sort removed cities by tour ordering
	
	# Create partial_tour by removing the selected cities from the original tour
	partial_tour = [city for city in tour if city not in removed_cities]
	
	# removed_cities_sorted = sorted(removed_cities, key=lambda city: tour.index(city))
	# cost_update = 0
	## Incremental cost update
	# for city in removed_cities_sorted:
	# 	cost_update += getCostUpdate(tour, city, cost, matrix)

	# 	partial_tour.remove(city)

	# return partial_tour, removed_cities, cost_update
	return partial_tour, removed_cities

# Removes the num_of_cities with highest cost
def destroyHighestCost(tour : list[int], num_of_cities : int, matrix : list[list[float]], cost : int):
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
	# Take first num_of_cities of the sorted path list
	removed_cities = [item[0] for item in sorted_dict][:num_of_cities]
	# Create the partial tour by trimming out the removed cities
	partial_tour = [city for city in tour if city not in removed_cities]

	return partial_tour, removed_cities

# TODO -> Doesn't work for highestrandom and cluster
def getCostUpdate(tour, city, cost, matrix):
	cost_deviation = 0
	# neighbors in the cyclic path
	i = tour.index(city)

	prev_city = tour[i - 1] if i > 0 else tour[-1]
	next_city = tour[(i + 1) % len(tour)]
	
	# Remove the cost contributions from the city and its neighbors
	cost_deviation -= matrix[prev_city][city] + matrix[city][next_city]
	
	# Add the new connection between previous and next city
	cost_deviation += matrix[prev_city][next_city]

	return cost_deviation