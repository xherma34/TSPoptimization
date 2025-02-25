import misc as m
import repair as r
import destroy as d
import time
import math
import random

# Simmulated annealing
def acceptWithProbability(best_cost, new_cost, temperature):
	cost_delta =  new_cost - best_cost
	probability = math.exp(-cost_delta / temperature)
	rng = random.random()
	return probability > rng

def lns(stoppage : int, initial_solution : list[int], matrix : list[list[float]],timeout: int, optimization: int, start_time : time) -> list[list[int],int]:
	# Setup counter for stagnation
	stag_runs_cnt = 0
	# Setup a threshold for how many iterations without improvement are okay

	threshold = 0.18 * stoppage
	# Calculate current cost of the tour
	best_cost = m.calculateCost(initial_solution, matrix)
	# Make a copy of initial tour and store it to best_tour
	best_s = initial_solution[:]
	# Save the number of elements in complete tour
	tour_len = len(initial_solution)
	
	# Parameters for destroy and repair
	destroy_method = "highestcost"
	repair_method = "random"
	# Calculate as  percentage of the len(tour) casted into integer
	destroy_size_perc = 30
	destroy_size  = int(len(initial_solution) * (destroy_size_perc / 100))
	stag_cnt = 0

	# simulate annealing variables
	initial_cost_delta = 0.1 * best_cost  # 10% increase in initial cost
	target_acceptance_probability = 0.5
	temperature = -initial_cost_delta / math.log(target_acceptance_probability)  # Higher initial temperature
	cooling_rate = 0.97  # Slightly slower cooling

	# Main loop
	for i in range(stoppage):
		elapsed = time.time()-start_time
		
		# if stagnation
		if stag_runs_cnt > threshold:
			# If stagnation happens, change the destroy and repair methods to be more aggresive
			# DESTROY -> bigger number of deleted cities
			destroy_size, destroy_size_perc = d.increaseDestroySize(destroy_size, destroy_size_perc, tour_len)
			destroy_method = "random"
			repair_method = "bestrandom"
			stag_cnt += 1
		
		# Destroy
		partial_solution, removed_cities = d.destroyMethod(best_s, destroy_size, destroy_method, matrix, best_cost)
		#if time is out
		if time.time() - start_time > timeout:
			break
		# Repair
		repaired_tour, repaired_cost = r.repairMethod(best_cost, partial_solution, removed_cities, repair_method, matrix)
		#if time is out
		if time.time() - start_time > timeout:
			break
		opt, opt_cost = m.get2opt(matrix, repaired_tour, repaired_cost, optimization, start_time, timeout)

		#if time is out
		if time.time() - start_time > timeout:
			break
		# Cost evaluation
		if opt_cost < best_cost:
			# Update
			best_s = opt
			best_cost = opt_cost
			stag_runs_cnt = 0
			destroy_method = "random"
			repair_method = "bestposition"
		else:
			# if accept_with_probability(temperature)
			if acceptWithProbability(best_cost, opt_cost, temperature):
				best_s = opt
				best_cost = opt_cost
			stag_runs_cnt += 1
		
		# Termination criteria if stagnation happens
		if stag_runs_cnt >= 0.55*stoppage:
			break

		temperature *= cooling_rate

	return best_s, best_cost