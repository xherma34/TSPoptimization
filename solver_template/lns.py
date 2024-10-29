import misc as m
import repair as r
import destroy as d
import time
import math
import random

def acceptWithProbability(best_cost, new_cost, temperature):
	cost_delta =  new_cost - best_cost
	probability = math.exp(-cost_delta / temperature)
	rng = random.random()
	# print(f"------------\nProbability of worse: {probability} \nrandom threshold: {rng} \nand delta is: {cost_delta}")
	# print(f"Temperature is: {temperature}\n------------")
	return probability > rng

def lns(stoppage : int, initial_solution : list[int], matrix : list[list[float]],timeout: int, optimization: int, start_time : time) -> list[list[int],int]:
	# Setup counter for stagnation
	stag_runs_cnt = 0
	# Setup a threshold for how many iterations without improvement are okay
	# TODO -> Uncomment
	# threshold = 0.25 * stoppage
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

	# simulate annealing variables
	initial_cost_delta = 0.1 * best_cost  # 10% increase in initial cost
	target_acceptance_probability = 0.5
	temperature = -initial_cost_delta / math.log(target_acceptance_probability)  # Higher initial temperature
	cooling_rate = 0.97  # Slightly slower cooling

	# temperature = 1/len(best_s) * best_cost
	# cooling_rate = 0.95
	# print(f"number of cities : {len(best_s)} with cost : {best_cost}")
	# print(f"temperature is: {temperature}")

	# DEBUG constants
	if_cnt = 0
	accepted_cnt = 0

	# Main loop
	for i in range(stoppage):
		elapsed = time.time()-start_time
		#if time is out
		if elapsed > timeout:
			print("Time limit is up")
			print(f"Iterations: {i}")
			break
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
		
		# m.calculateCost na partial solution, m.calculateCost na best_s a odecist
		# Srovnat s best_cost
		# print(f"Cost of solution: {m.calculateCost(best_s, matrix)}")
		# Destroy
		partial_solution, removed_cities = d.destroyMethod(best_s, destroy_size, destroy_method, matrix, best_cost)
		# Repair
		repaired_tour, repaired_cost = r.repairMethod(best_cost, partial_solution, removed_cities, repair_method, matrix)
		opt, opt_cost = m.get2opt(matrix, repaired_tour, repaired_cost, optimization)



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
				accepted_cnt += 1
				best_s = opt
				best_cost = opt_cost
			if_cnt += 1
			stag_runs_cnt += 1

		# TODO -> stagnation -> terminate

		temperature *= cooling_rate

	# print(f"Number of stagnations: {if_cnt} out of total runs {stoppage} that is {(if_cnt/stoppage)*100}%")
	# print(f"Number of accepted worse tours: {accepted_cnt} out of total ifs {if_cnt} that is {(accepted_cnt/if_cnt)*100}%")

	return best_s, best_cost

def test(initial_solution, matrix, cost):
	partial, removed, cost_dev = d.destroyTest(matrix, cost, initial_solution)
	print(f"DESTROY: Returned partial: {partial}")
	print(f"DESTROY: Returned cost after remove: {cost_dev+cost}")
	print(f"DESTROY: m.calcCost output on partial: {m.calculateCost(partial, matrix)}")

	new_cost = cost+cost_dev

	new_s, new_c_d = r.repairTest(new_cost, partial, removed, matrix)
	print(f"REPAIRD: Returned repaired: {new_s}")
	print(f"DESTROY: Returned cost after repair: {new_cost+new_c_d}")
	print(f"DESTROY: m.calcCost output on partial: {m.calculateCost(new_s, matrix)}")
