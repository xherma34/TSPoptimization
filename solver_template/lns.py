import misc as m
import repair as r
import destroy as d

# TODO -> FIX: somehow even when changing the destroy method to clusters
def lns(stoppage : int, initial_solution : list[int], matrix : list[list[float]]) -> list[list[int],int]:
	# Setup counter for stagnation
	stag_runs_cnt = 0
	# Setup a threshold for how many iterations without improvement are okay
	threshold = 10
	# Calculate current cost of the tour
	best_cost = m.calculateCost(initial_solution, matrix)
	# Make a copy of initial tour and store it to best_tour
	best_s = initial_solution[:]
	# Save the number of elements in complete tour
	tour_len = len(initial_solution)
	
	# Parameters for destroy and repair
	destroy_method = "random"
	repair_method = "bestposition"
	# Calculate as  percentage of the len(tour) casted into integer
	destroy_size_perc = 30
	destroy_size  = int(len(initial_solution) * (destroy_size_perc / 100))
	stag_cnt = 0

	# Main loop
	for i in range(stoppage):
		# if stagnation
		if stag_runs_cnt > threshold:
			# If stagnation happens, change the destroy and repair methods to be more aggresive
			# DESTROY -> bigger number of deleted cities
			destroy_size, destroy_size_perc = d.increaseDestroySize(destroy_size, destroy_size_perc, tour_len)
			# DESTROY_METHOD, REPAIR_METHOD -> something that will take me out of the local optima
			destroy_method = "highestcost"
			# TODO -> think about doing regret k-insertion 
			repair_method = "bestrandom"
			stag_cnt += 1

		# Destroy
		partial_solution, removed_cities = d.destroyMethod(best_s, destroy_size, destroy_method, matrix)
		# Repair
		repaired_tour, repaired_cost = r.repairMethod(partial_solution, removed_cities, repair_method, matrix)
		

		# TODO -> 2-opt
		opt, opt_cost = m.get2opt(matrix, repaired_tour, 10)
		#print(repaired_tour, opt)
		#print(repaired_cost, opt_cost)


		# Cost evaluation
		if opt_cost < best_cost:
			# Update
			best_s = opt
			best_cost = opt_cost
			stag_runs_cnt = 0
			destroy_method = "random"
			repair_method = "bestposition"
		else:
			stag_runs_cnt += 1
		# else
			# TODO -> maybe if we struggle we can do simmulated annealing to not get stuck on local optima
			# SIMMULATED ANNEALING:
				# if random < acceptance_prob
					# accept new solution
				# else  		 
					# stagnation counter ++
		# temperature += cooling_rate
		# 
	return best_s, best_cost

# #TODO finish LNS implementation
# def lns( stopage: int, matrix: list[list[float]], solution: list[int]) ->list[list[int],int]:
#     s = solution
#     best_s = s
#     best_cost = m.calculateCost(best_s,matrix)

#     for i in range(stopage):
#         #destroy
#         #repair
#         #2-opt
#         #new cost
#         #update
#         #solution acceptance
#         pass
#     return best_s, best_cost